import json
from datetime import date, datetime

from dateutil.tz import tzutc

from notion_objects import (
    DateRangeEnd,
    DateRangeStart,
    DynamicNotionObject,
    MultiSelect,
    NotionObject,
    Page,
    Person,
    Phone,
    Select,
    Status,
    TitlePlainText,
)

query_result = '{"object":"list","results":[{"object":"page","id":"390100a5-4808-1234-b8b4-87352b65c403","created_time":"2022-10-08T22:29:00.000Z","last_edited_time":"2022-10-09T00:48:00.000Z","created_by":{"object":"user","id":"3fd2f9aa-a320-4e7d-83a2-f489299a3328"},"last_edited_by":{"object":"user","id":"3fd2f9aa-xxxx-xxxx-xxxx-f489299a3328"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"9b5xxxxc-0xxd-4xxx-accc-6fabacabbaab"},"archived":false,"properties":{"My select":{"id":"Hs%5Dj","type":"select","select":{"id":"ffc9b948-864c-4044-aff2-27fed1df1427","name":"b","color":"purple"}},"Created time":{"id":"Jv%60q","type":"created_time","created_time":"2022-10-08T22:29:00.000Z"},"Person":{"id":"WC%5CO","type":"people","people":[]},"Status":{"id":"%5DvNj","type":"status","status":null},"Date":{"id":"_PPi","type":"date","date":null},"Tags":{"id":"sAAp","type":"multi_select","multi_select":[]},"Phone":{"id":"zd%3AH","type":"phone_number","phone_number":"+10900234123"},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"a second page","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"a second page","href":null}]}},"url":"https://www.notion.so/a-second-page-390100a548084236b8b487352b65c403"},{"object":"page","id":"5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9","created_time":"2022-10-08T22:29:00.000Z","last_edited_time":"2022-10-09T00:48:00.000Z","created_by":{"object":"user","id":"3fd2f9aa-a320-4e7d-83a2-f489299a3328"},"last_edited_by":{"object":"user","id":"3fd2f9aa-a320-4e7d-83a2-f489299a3328"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"9b5154dc-cccc-bbbb-aaaa-123124234cad"},"archived":false,"properties":{"My select":{"id":"Hs%5Dj","type":"select","select":{"id":"90d37b63-e696-49f7-a361-73de72250ced","name":"a","color":"yellow"}},"Created time":{"id":"Jv%60q","type":"created_time","created_time":"2022-10-08T22:29:00.000Z"},"Person":{"id":"WC%5CO","type":"people","people":[{"object":"user","id":"3fd2f9aa-a320-4e7d-83a2-f489299a3328","name":"Thomas","avatar_url":"https://s3-us-west-2.amazonaws.com/public.notion-static.com/e10406d1-04a6-4c0c-bf29-d875c5abe86e/portrait-square.jpg","type":"person","person":{"email":"thomas@localstack.cloud"}}]},"Status":{"id":"%5DvNj","type":"status","status":{"id":"8a9dd46d-625f-470e-91ef-dd16a1e9dfa4","name":"In progress","color":"blue"}},"Date":{"id":"_PPi","type":"date","date":{"start":"2022-10-09","end":"2022-10-09","time_zone":null}},"Tags":{"id":"sAAp","type":"multi_select","multi_select":[{"id":"a292acc3-f4f2-4ead-ba9f-6b83e4c26ed1","name":"foobar","color":"purple"},{"id":"859ece03-2b87-4522-a152-9d147482eebe","name":"baz","color":"green"}]},"Phone":{"id":"zd%3AH","type":"phone_number","phone_number":"+4369912345678"},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"A page","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"A page","href":null}]}},"url":"https://www.notion.so/A-page-5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx9"}],"next_cursor":null,"has_more":false,"type":"page","page":{}}'


class SampleObject(NotionObject):
    name = TitlePlainText("Name")
    status = Status("Status")
    person = Person("Person")
    my_select = Select("My select")
    date_start = DateRangeStart("Date")
    date_end = DateRangeEnd("Date")
    Phone = Phone()
    Tags = MultiSelect()


class SamplePage(Page, SampleObject):
    """Like SampleObject but also includes Page properties"""


def test_access_properties():
    data = json.loads(query_result)["results"]

    o = SampleObject(data[1])
    assert o.name == "A page"
    assert o.person == "Thomas"
    assert o.status == "In progress"
    assert o.my_select == "a"
    assert o.date_start
    assert o.date_end
    assert o.Phone == "+4369912345678"
    assert o.Tags == ["foobar", "baz"]

    o = SampleObject(data[0])
    assert o.name == "a second page"
    assert o.person is None
    assert o.status is None
    assert o.my_select == "b"
    assert o.date_start is None
    assert o.date_end is None
    assert o.Phone == "+10900234123"
    assert o.Tags == []


def test_set_properties():
    data = json.loads(query_result)["results"]

    o = SampleObject(data[1])

    o.status = "Closed"
    print(o.__changes__)


def test_to_dict():
    data = json.loads(query_result)["results"]

    o = SampleObject(data[1])
    assert o.to_dict() == {
        "name": "A page",
        "person": "Thomas",
        "status": "In progress",
        "my_select": "a",
        "date_end": date(2022, 10, 9),
        "date_start": date(2022, 10, 9),
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }
    assert o.to_dict(flat=True) == {
        "name": "A page",
        "person": "Thomas",
        "status": "In progress",
        "my_select": "a",
        "date_end": date(2022, 10, 9),
        "date_start": date(2022, 10, 9),
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }

    o = SamplePage(data[1])
    assert o.to_dict() == {
        "id": "5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9",
        "last_edited_time": datetime(2022, 10, 9, 0, 48, tzinfo=tzutc()),
        "created_time": datetime(2022, 10, 8, 22, 29, tzinfo=tzutc()),
        "name": "A page",
        "person": "Thomas",
        "status": "In progress",
        "my_select": "a",
        "date_end": date(2022, 10, 9),
        "date_start": date(2022, 10, 9),
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }


def test_dynamic_notion_object_to_dict():
    data = json.loads(query_result)["results"]

    o = DynamicNotionObject(data[1])
    assert o.to_dict() == {
        "id": "5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9",
        "created_time": datetime(2022, 10, 8, 22, 29, tzinfo=tzutc()),
        "last_edited_time": datetime(2022, 10, 9, 0, 48, tzinfo=tzutc()),
        "Created time": datetime(2022, 10, 8, 22, 29, tzinfo=tzutc()),
        "Date": {"start": date(2022, 10, 9), "end": date(2022, 10, 9)},
        "Name": "A page",
        "Person": ["Thomas"],
        "Status": "In progress",
        "My select": "a",
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }

    assert o.to_dict(flat=True) == {
        "id": "5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9",
        "created_time": datetime(2022, 10, 8, 22, 29, tzinfo=tzutc()),
        "last_edited_time": datetime(2022, 10, 9, 0, 48, tzinfo=tzutc()),
        "Created time": datetime(2022, 10, 8, 22, 29, tzinfo=tzutc()),
        "Date_start": date(2022, 10, 9),
        "Date_end": date(2022, 10, 9),
        "Name": "A page",
        "Person": ["Thomas"],
        "Status": "In progress",
        "My select": "a",
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }


def test_dynamic_notion_object_to_json():
    data = json.loads(query_result)["results"]

    o = DynamicNotionObject(data[1])
    assert json.loads(o.to_json()) == {
        "id": "5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9",
        "created_time": "2022-10-08T22:29:00+00:00",
        "last_edited_time": "2022-10-09T00:48:00+00:00",
        "Created time": "2022-10-08T22:29:00+00:00",
        "Date": {"start": "2022-10-09", "end": "2022-10-09"},
        "Name": "A page",
        "Person": ["Thomas"],
        "Status": "In progress",
        "My select": "a",
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }

    assert json.loads(o.to_json(flat=True)) == {
        "id": "5ddfefe3-9868-4dd9-88bf-5c9849f8b4e9",
        "created_time": "2022-10-08T22:29:00+00:00",
        "last_edited_time": "2022-10-09T00:48:00+00:00",
        "Created time": "2022-10-08T22:29:00+00:00",
        "Date_start": "2022-10-09",
        "Date_end": "2022-10-09",
        "Name": "A page",
        "Person": ["Thomas"],
        "Status": "In progress",
        "My select": "a",
        "Phone": "+4369912345678",
        "Tags": ["foobar", "baz"],
    }
