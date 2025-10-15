# Author: Sergio Stinchi

# Version        Description
# 2.0.0          Allow the script to setup more role for user
# 1.2.0          Moved clearCache after syncronization          
# 1.1.1          Added Map RefreashAll AuthorizationGroupManager
# 1.1.0          Added Map role To Users
# 1.0.1          Added Mapping member to a group
# 1.0.0          Starting version

import sys
import java


# Global variables
scriptName = "createGroupsAndUsers.py"
version = "2.0.0"


# Auxiliary functions
# settings
groups = ['Group_1','Group_2']                                              # optional
users = [ ['UserTest',' password','name','surname',''] ]                    # optional  ['UID','Password','Name','Surname','MAIL' ]
userToGroups = [['UserTest','Group_1']]                                     #userToGroups = [['','']]   # optional ['userName','groupName']
UsersToRoles =[['UserTest',['administrator','adminsecuritymanager']]]       #UsersToRoles =[['UserTest',['ROLE_1','ROLE_2']]]
# Auxiliary functions

def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def clearCache():
     secList= AdminControl.queryNames('type=SecurityAdmin,*')
     for sec in secList.splitlines():
        AdminControl.invoke(sec,'clearAuthCache')

     agBeanList = AdminControl.queryNames('type=AuthorizationGroupManager,process=dmgr,*')
     for agBean in agBeanList.splitlines():
        AdminControl.invoke(agBean, 'refreshAll') 



def listRolebyUser(user):
    roleAuthGroupList = []
    authorizationGroups  = AdminTask.listAuthorizationGroupsForUserID('[-userid %s]' %(user))
    #print "authorizationGroups %s " %authorizationGroups
    roleTable = authorizationGroups[1:len(authorizationGroups) -1].split(",")
    #print "roleTable size  = %s " %(len(roleTable))
    #print "roleTable = %s " %roleTable
    
    for role in roleTable:
        if (len(role.split("=")[1])>2):
        #   print "role checked = %s" %(role)
            role = role + "]"
            #endIf  
            # Find role name and authorization group name 
            rolename = role[0:role.find("=")]
            #print "roleName = %s" %rolename
            authgroup = role[len(rolename)+2:len(role)-1]
            #print "authgroup = %s" %authgroup
            if len(authgroup)>0:
        #      print "Add Role %s to RoleGroup for user %s "  %(rolename,user)
               roleAuthGroupList.append(rolename.strip())
    #print "List Role = %s " %roleAuthGroupList   
    return roleAuthGroupList

def checkIfRoleIsAlreadyPresent(role,rolesArolesApplied):
    for item in rolesArolesApplied:
       if item == role:
          return  'True'; 
          break
        


# Command Line
argc = len(sys.argv)
if argc != 1:
   print "Usage: %s <target data file>" % (scriptName)
   sys.exit(-1)


# Start
print "%s V%s" % (scriptName, version)

# Read target data file

print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"


# Check data read
print "Check data read ..."

if len(users) == 0:
   print "ERROR: The variable users is mandatory"
   print "%s done" % scriptName
   sys.exit(-1)
if isinstance(users, type([])) == 0:
      print "ERROR: The variable users must be a list"
      print "%s done" % (scriptName)
      sys.exit(-1)
for dummy in users:
   if isinstance(dummy, type([])) == 0 or len(dummy) != 5:
      print "ERROR: Each object of variable users must be a list of a 4 elements"
      print "%s done" % (scriptName)
      sys.exit(-1)      
  
  
if isinstance(UsersToRoles, type([])) == 0:
   print "ERROR: The variable users must be a list"
   print "%s done" % scriptName
   sys.exit(-1)
else:
   for dummy in  UsersToRoles:
      roles = dummy[1]
      #print "roles = %s " % (roles)
      for role in roles:
          #print "role = %s " % (role)
          if role not in ['administrator','monitor','configurator','operator','deployer','auditor','adminsecuritymanager']:
             print "ERROR: Role must be one of These: [administrator, monitor, configurator,operator,deployer,auditor,adminsecuritymanager]"
             sys.exit(-1)

try:
    print " "
    print "===== User Creation ====== " 
    for user in users:
      #Create User
      print "Create User: %s" %(user[0]) ,
      #check if user exist 
      usr=AdminTask.searchUsers(['-uid', user[0]])
      #print "usr = %s " % usr
      if len(usr) > 0:
        print " already  exist - creation skipped " 
      else:
         if len (user[2])==0: cn=user[0] 
         else: cn=user[2]
         if len (user[3])==0: sn=user[0] 
         else: sn=user[3]
         AdminTask.createUser (['-uid', user[0], '-password', user[1], '-confirmPassword', user[1], '-cn', cn, '-sn', sn, '-mail', user[4]])
         print " OK "
    
    print " "
    print "===== Role Configuration ====== "
    for userToRoles in UsersToRoles:
       user = userToRoles[0]
       roles = userToRoles[1]
       #print "role for users %s are %s" % (user,listRolebyUser(user))
       for role in roles:
          print "Apply Role:'%s' to User:'%s'"  % (role,user),
          rolesApplied = listRolebyUser(user)
          ret=checkIfRoleIsAlreadyPresent(role,rolesApplied)
          if ret=='True':
              print " The Role is already present - skipped Association" 
          else:
              res = AdminTask.mapUsersToAdminRole('[-roleName %s -userids [%s]]' % (role,user))
              print " OK"
    
    print " "
    print "===== Group Creation ====== "
    for group in groups:
      #create Group
      print "Create Group:  %s " %(group) ,
      #check if group exist
      grp = AdminTask.searchGroups(['-cn', group]) 
      if len(grp) > 0:
         print "The Group already  exist , creation skipped "
      else:
         AdminTask.createGroup (['-cn', group, '-description', group])
         print " OK"

    print " "
    print "===== Group Association ====== "
    for userToGroup in userToGroups:
      # Map user to Group
      print "Map user %s to Group %s " %(userToGroup[0],userToGroup[1]), 
      memberUniqueName=AdminTask.searchUsers(['-uid', userToGroup[0]])
      groupUniqueName= AdminTask.searchGroups(['-cn', userToGroup[1]])
      AdminTask.addMemberToGroup ('[-memberUniqueName ' +memberUniqueName + ' -groupUniqueName  ' + groupUniqueName + ']')
      print " OK"
except:
      print " KO"
      type, value, traceback = sys.exc_info()
      print "ERROR: %s (%s)" % (str(value), type)
      clearExit(" - KO: Rollback and exit", -1)


print " "
print "createGroupsAndUsers done "
      
if AdminConfig.hasChanges() == 1:
   # Save
   print "Save ..."
   AdminConfig.save()
   print "Save done"
   # Synchronization
   print "Synchronization ..."
   nodes = AdminControl.queryNames('type=NodeSync,*')
   if len(nodes) > 0:
      nodelist = nodes.split(lineSeparator)
      if len(nodelist) > 0:
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
# Done
print "Reload Security Cache"
clearCache()
print "%s done" % scriptName      
