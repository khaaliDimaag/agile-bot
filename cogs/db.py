import pymongo, bson

from pymongo import MongoClient
client = MongoClient()

''' [DB] khaaliDiscord:
[Collection] members: {
  name: str,
  handle: str,
  joined: date,
  left: date,
  bot: boolean
}
[Collection] channels: {
  name: str,
  purpose: str,
  private: boolean
}
[Collection] roles: {
  name: str,
  purpose: str
}
'''
guild = client['khaaliDiscord']

''' [DB] khaaliProjects:
[Collection] projects: {
  name: str,
  repo: url,
  start: date,
  release: str,
  product_backlog: [],
  release_backlog: [],
  sprints: []
}
[Collection] stories: {
  inshort: str,
  details: str,
  project: ObjectID,
  parents: [],
  children: [],
  added: date,
  timereq: int,
  timeleft: int
}
[Collection] sprints: {
  project: ObjectID,
  number: int,
  start: date,
  end: date,
  stories: [],
  incomplete: [],
  review: str
}
'''
projects = client['khaaliProjects']