import inspect
import struct
import logging

from . import frames

logger = logging.getLogger("HAL.Frames")

class FrameError(Exception):
    pass

class InvalidFrameTypeError(FrameError):
    pass

class InvalidLengthError(FrameError):
    pass


class Frame:

    type_ = None

    def pack(self):
        raise NotImplementedError()

    @classmethod
    def unpack(cls, buff):
        raise NotImplementedError()




class InitFrame(Frame):

    type_ = 1 << 7

class InitDrive(Frame):

    type_ = InitFrame.type_ + 1

    @classmethod
    def pack(cls):
        # never anything after the header, size is alway 0
        return struct.pack("!BB", cls.type_, 0)

    @classmethod
    def unpack(cls, buff):
        if len(buff):
            raise InvalidLengthError(
                "Length should be 0 not {}".format(len(buff)))

        return cls()


# in an Effort to keep this DRY.

frames = [x[1] for x in inspect.getmembers(frames)
          if inspect.isclass(x[1]) and
             issubclass(x[1], Frame)]

type_lookup = {x.type_ : x for x in frames}


def unpack(buff):
    #This assumes the start of a frame.

    if len(buff) < 2:
        logging.info("too short to parse into packet, returning")
        return None, buff

    pkt_type, len_ = struct.unpack("!BB", buff[:2])
    logging.info("Got packet type:{}".format(pkt_type))

    if pkt_type not in type_lookup:
        print(type_lookup)
        raise InvalidFrameTypeError(
            "Can't process frame type: {}".format(pkt_type))

    if len(buff) < len_ -2:
        return None, buff

    buff = buff[2:]

    cls = type_lookup[pkt_type]
    pkt = cls.unpack(buff[:len_])

    buff = buff[len_:]
    return pkt, buff

