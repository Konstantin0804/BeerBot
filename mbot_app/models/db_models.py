from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import inspect


@dataclass
class Container:
    id: int
    item_id: int
    container_size_id: int
    price: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class TapItem:
    id: int
    name: str
    style: str
    brewery: str
    abv: str
    ibu: str
    label_image_hd: str
    position: int
    containers: List[Container]
    price: str = field(default=None, init=False)

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    def __post_init__(self):
        try:
            self.price = self.containers[0]['price']
        except IndexError:
            self.price = '0.0'
        if not self.price:
            self.price = '--'
        all_containers = []
        for container in self.containers:
            all_containers.append(Container.from_dict(container))
        self.containers = all_containers

    def repr_necessary_data(self):
        repr_dict = self.__dict__
        for e in ['position', 'containers']:
            repr_dict.pop(e)
        return repr_dict


@dataclass
class Section:
    id: int
    menu_id: int
    position: int
    name: str
    description: bool
    type: str
    public: bool
    created_at: datetime
    updated_at: datetime
    items: List[TapItem]

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    def __post_init__(self):
        all_items = []
        for item in self.items:
            all_items.append(TapItem.from_dict(item))
        self.items = all_items


@dataclass
class Menu:
    id: int
    location_id: int
    uuid: str
    name: str
    draft: bool
    unpublished: bool
    position: int
    show_price_on_untappd: bool
    push_notification_frequency: str
    created_at: datetime
    updated_at: datetime
    sections: List[Section]
    on_deck_section: Section
    description: Optional[str] = None
    footer: Optional[str] = None

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    def __post_init__(self):
        self.on_deck_section = Section(**self.on_deck_section)
        all_sections = []
        for section in self.sections:
            all_sections.append(Section(**section))
        self.sections = all_sections


@dataclass
class Tap:
    menu: List[Menu]
    _id: datetime = field(default=None, init=False)
    act_flg: int = field(default=None, init=False)

    def __post_init__(self):
        self._id = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if not self._id else self._id
        self.act_flg = 1 if not self.act_flg else self.act_flg

