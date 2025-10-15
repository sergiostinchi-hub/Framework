# Variables
scriptName = "SyncEnv.py"
version = "1.0.5"
print "Synchronization ..."
nodes = AdminControl.queryNames('type=NodeSync,*')
if len(nodes) > 0:
   nodelist = nodes.splitlines()      
   for node in nodelist:
      beg = node.find('node=') + 5
      end = node.find(',', beg)
      print "Synchronization for node \"" + node[beg:end] + "\" :",
      try: AdminControl.invoke(node, 'sync')
      except: print "KO"
      else: print "OK"
else:
   print "No running nodeagents found"
print "Synchronization done"
