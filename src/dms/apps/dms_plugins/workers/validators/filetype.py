import magic
from dms_plugins.workers import PluginError

MIMETYPES = [
                ('application/pdf', 'pdf'),
                ('image/tiff', 'tiff'),
                ('image/jpeg', 'jpg'),
                ('image/gif', 'gif'),
                ('image/png', 'png'),
                ('text/plain', 'txt'),
                ('application/msword', 'doc'),
                ('application/vnd.ms-excel', 'xls'),
            ]

def get_mimetypes():
    return [ x[0] for x in MIMETYPES ]

class FileTypeValidationWorker(object):
    mimetypes = get_mimetypes()
    
    def work(self, request, document, **kwargs):
        filebuffer = document.get_uploaded_file()
        if filebuffer is None:
            raise PluginError('File buffer not initialized')
        mime = magic.Magic( mime=True )
        typ = mime.from_buffer( filebuffer.read() )
        if not typ in self.mimetypes:
            raise PluginError('File type %s is not supported' % typ)
        return document