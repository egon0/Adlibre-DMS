from dms_plugins.workers.storage import local
from dms_plugins.workers.validators import filetype
from dms_plugins.workers.security import groups, hashcode
from dms_plugins.workers.transfer import gzip
from dms_plugins.pluginpoints import BeforeStoragePluginPoint, BeforeRetrievalPluginPoint

"""
Plugin interface:

Attrs:
    title (default == '')
    description (default == '')
    active (default == False)
    order (default == 0)

Methods:
    work (must return document in some form)

"""

class FileTypeValidationPlugin(BeforeStoragePluginPoint):
    title = "File Type Validator"
    description = "Validates document type against supported types"
    active = True
    
    def work(self, request, document):
        return filetype.FileTypeValidationWorker().work(request, document)

class HashCodeValidationPlugin(BeforeRetrievalPluginPoint):
    name = 'Hash'
    description = 'Hash code validation on retrieval'
    #has_configuration = True #TODO: configuration

class LocalStoragePlugin(BeforeStoragePluginPoint):
    title = "Local Storage"
    description = "Saves document as local file"
    active = True

    def work(self, request, document, **kwargs):
        return local.Local().store(request, document)

class GroupSecurityStore(BeforeStoragePluginPoint):
    name = 'Security Group'
    description = 'Security group member only'
    active = True

    def work(self, request, document):
        return groups.GroupSecurityWorker().work(request, document)

class GroupSecurityRetrieval(BeforeRetrievalPluginPoint):
    name = 'Security Group'
    description = 'Security group member only'
    active = True

    def work(self, request, document):
        return groups.GroupSecurityWorker().work(request, document)

class GzipOnStorePlugin(BeforeStoragePluginPoint):
    title = 'Gzip Plugin'
    active = True
    #has_configuration = True #TODO: configure
    
    def work(self, request, document):
        return gzip.GzipWorker.work_store(request, document)

class GzipOnRetrievePlugin(BeforeRetrievalPluginPoint):
    title = 'Gzip Plugin'
    active = True
    #has_configuration = True #TODO: configure

    def work(self, request, document):
        return gzip.GzipWorker.work_retrieve(request, document)