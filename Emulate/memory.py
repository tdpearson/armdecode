import os
import pickle
import lzma

class Memory(object):
    def __init__(self):
        self.page_size = 1024 ** 2  # 1MB
        self.page = {}

    def _getpage(self, position):
        return position // self.page_size

    def _getpageoffset(self, position):
        return position - (self.page_size * self._getpage(position))

    def read(self, position):
        page = self._getpage(position)
        offset = self._getpageoffset(position)
        try:
            return self.page[page][offset]
        except KeyError:
            return 0  # assuming uninitiated values are READ AS ZERO

    def read_blob(self, size, position, buffer=b''):
        page = self._getpage(position)
        offset = self._getpageoffset(position)
        if size + offset > self.page_size:
            split_point = self.page_size - offset
            try:
                buffer += self.page[page][offset:]
            except KeyError:
                # We are reading in an uninitiated page - assume read as zeros
                buffer += bytearray(split_point)
            size -= split_point
            position += split_point
            return self.read_blob(size, position, buffer)
        try:
            return bytearray(buffer + self.page[page][offset:offset + size])
        except KeyError:
            # We are reading in an uninitiated page
            return bytearray(buffer + bytearray(size))

    def write(self, byte, position):
        page = self._getpage(position)
        offset = self._getpageoffset(position)
        try:
            self.page[page][offset:offset + 1] = byte
        except KeyError:
            self.page[page] = bytearray(self.page_size)
            self.page[page][offset:offset + 1] = byte

    def write_blob(self, bytedata, position):
        page = self._getpage(position)
        offset = self._getpageoffset(position)
        data_length = len(bytedata)
        # write data that spans pages to the corresponding pages
        if data_length + offset > self.page_size:
            split_point = self.page_size - offset
            self.write_blob(bytedata[split_point:], (page + 1) * self.page_size)
            bytedata = bytedata[:split_point]
        try:
            self.page[page][offset:offset + data_length] = bytedata
        except KeyError:
            self.page[page] = bytearray(self.page_size)
            self.page[page][offset:offset + data_length] = bytedata
        # print('writing %s to page %s' % (bytedata, page))

    def save_page(self, page_number, filename):
        with open(filename, 'wb') as f:
            f.write(self.page[page_number])

    def load_page(self, page_number, filename):
        file_size = os.path.getsize(filename)
        if file_size > self.page_size:
            raise OverflowError('page file larger than page size')
        with open(filename, 'rb') as f:
            self.page[page_number] = bytearray(self.page_size)
            f.readinto(self.page[page_number])

    def save_state(self, filename):
        with open(filename, 'wb') as f:
            f.write(lzma.compress(pickle.dumps(self.page)))

    def load_state(self, filename):
        with open(filename, 'rb') as f:
            self.page = pickle.loads(lzma.decompress(f.read()))