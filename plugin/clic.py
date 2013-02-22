from clang.cindex import *
import vim
import bsddb.db as db
import linecache

def getCurrentLine():
  return int(vim.eval("line('.')"))

def getCurrentColumn():
  return int(vim.eval("col('.')"))

def getCurrentUsr():
  userOptionsGlobal = splitOptions(vim.eval("g:clang_user_options"))
  userOptionsLocal = splitOptions(vim.eval("b:clang_user_options"))
  args = userOptionsGlobal + userOptionsLocal
  tu = getCurrentTranslationUnit(args, getCurrentFile(), vim.current.buffer.name, update = True)
  file = tu.getFile(vim.current.buffer.name)
  loc = tu.getLocation(file, getCurrentLine(), getCurrentColumn())
  cursor = tu.getCursor(loc)
  ref = None
  while (ref is None or ref == Cursor.nullCursor()):
    ref = cursor.get_ref()
    nextCursor = cursor.get_lexical_parent()
    if (nextCursor is None or cursor == nextCursor):
      return None
    cursor = nextCursor
  return ref.get_usr()

# searchKind is one of ["declarations", "subclasses", None]
def getCurrentReferences(searchKind = None):
  def loadClic():
    filename = vim.eval("expand(g:clic_filename)")
    clicDb = db.DB()
    try:
      clicDb.open(filename, None, db.DB_BTREE, db.DB_RDONLY)
      return clicDb
    except db.DBNoSuchFileError:
      print "DBNoSuchFileError", filename
      clicDb.close()
      return None

  def getReferencesForUsr(clicDb, usr):
    locations = clicDb.get(usr, '')
    return locations.split('\t')

  def locationToQuickFix(location):
    parts = location.split(':')
    if len(parts) != 4:
      return {} # mark invalid items with an empty dict
    filename = parts[0]
    line = int(parts[1])
    column = int(parts[2])
    kind = int(parts[3])
    refKind  = referenceKinds[kind] or kind
    text = linecache.getline(filename, line).rstrip('\n')
    if text is not '':
        text = refKind.rstrip() + ": " + text.strip()
    return {'filename' : filename, 'lnum' : line, 'col' : column, 'text': text, 'kind': kind}

  def filtered(quickFixList):
    quickFixList = filter(lambda x: len(x) > 0 and len(x['text']) > 0, quickFixList) # remove invalid items
    vaildKinds = []
    if searchKind == None:
      return quickFixList
    elif searchKind == 'declarations':
      validKinds = range(1, 40)
    elif searchKind == 'subclasses':
      validKinds = [44]
    return filter(lambda x: x['kind'] in validKinds, quickFixList)

  def deduplicated(quickFixList):
    def locationsMatch(item1, item2):
      return item1['filename'] == item2['filename']\
          and item1['lnum'] == item2['lnum']\
          and item1['col'] == item2['col']
    i = 0
    while i < len(quickFixList):
      if i > 0 and locationsMatch(quickFixList[i], quickFixList[i-1]):
        # In general, a Kind of higher value is more interesting,
        # so we deduplicate the list by removing the Kind of lower value
        # when we see two adjacent items at the same location
        if quickFixList[i-1]['kind'] < quickFixList[i]['kind']:
          quickFixList.pop(i-1)
        else:
          quickFixList.pop(i)
      else:
        i += 1
    return quickFixList

  # Start of getCurrentReferences():
  clicDb = loadClic()
  if clicDb is None:
    print "CLIC not loaded"
    return []
  usr = getCurrentUsr()
  if usr is None:
    print "No USR found"
    result = []
  else:
    result = filtered(map(locationToQuickFix, getReferencesForUsr(clicDb, usr)))
    result.sort(lambda a, b: cmp((a['filename'], a['lnum'], a['col'], a['kind']),
                                 (b['filename'], b['lnum'], b['col'], b['kind'])))
    result = deduplicated(result)
    if not result:
      print ("No subclasses " if searchKind == 'subclasses' else "No references to ") + usr
  clicDb.close()
  return result

referenceKinds = dict({
 1 : 'type declaration',
 2 : 'type declaration',
 3 : 'type declaration',
 4 : 'type declaration',
 5 : 'type declaration',
 6 : 'member declaration',
 7 : 'enum declaration',
 8 : 'function declaration',
 9 : 'variable declaration',
10 : 'argument declaration',
20 : 'typedef declaration',
21 : 'method declaration',
22 : 'namespace declaration',
24 : 'constructor declaration',
25 : 'destructor declaration',
26 : 'conversion function declaration',
27 : 'template type parameter',
28 : 'non-type template parameter',
29 : 'template template parameter',
30 : 'function template declaration',
31 : 'class template declaration',
32 : 'class template partial specialization',
33 : 'namespace alias',
43 : 'type reference',
44 : 'base specifier',
45 : 'template reference',
46 : 'namespace reference',
47 : 'member reference',
48 : 'label reference',
49 : 'overloaded declaration reference',
100 : 'expression',
101 : 'reference',
102 : 'member reference',
103 : 'function call'
})
