# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.cover.tiles.list import ListTile, IListTile
from plone.uuid.interfaces import IUUID
from plone.tiles.interfaces import ITileDataManager
from plone.app.uuid.utils import uuidToObject


class ICarouselTile(IListTile):
    """
    """


class CarouselTile(ListTile):
    index = ViewPageTemplateFile("templates/carousel.pt")
    is_configurable = False
    is_editable = False

    def populate_with_object(self, obj):
        super(ListTile, self).populate_with_object(obj)  # check permission
        try:
            image_size = obj.restrictedTraverse('@@images').getImageSize()
        except:
            image_size = None
        if not image_size:
            return
        self.set_limit()
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        if data_mgr.get()['uuids']:
            uuids = data_mgr.get()['uuids']
            if type(uuids) != list:
                uuids = [uuid]
            elif uuid not in uuids:
                uuids.append(uuid)

            old_data['uuids'] = uuids[:self.limit]
        else:
            old_data['uuids'] = [uuid]
        data_mgr.set(old_data)
