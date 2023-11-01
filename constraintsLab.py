#!/usr/bin/env python3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import constraint
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Task 1    
def Travellers(pairList):
  problem = constraint.Problem()
  people = ['claude', 'olga', 'pablo', 'scott']
  times = ['2:30', '3:30', '4:30', '5:30']
  destinations = ['peru', 'romania', 'taiwan', 'yemen']
  t_variables= list(map(( lambda x: 't_'+x ), people))
  d_variables= list(map(( lambda x: 'd_'+x ), people))
  problem.addVariables(t_variables, times)
  problem.addVariables(d_variables, destinations)
  # no two travellers depart at the same time
  problem.addConstraint(constraint.AllDifferentConstraint(), t_variables)
# no two travellers return from the same destination
  problem.addConstraint(constraint.AllDifferentConstraint(), d_variables)
  # Olga is leaving 2 hours before the traveller from Yemen
  for person in people:
    problem.addConstraint((
    lambda x,y,z:
    (y != 'yemen')
    or ((x == '4:30') and (z == '2:30'))
    or ((x == '5:30') and (z == '3:30'))
    ), ['t_'+person, 'd_'+person, 't_olga'])

  # Claude is either the person leaving at 2:30 pm or the traveller leaving at 3:30 pm.
  problem.addConstraint((
  lambda x:
  (x == '2:30') or (x == '3:30')
  ), [ 't_claude'])

  # The person leaving at 2:30 pm is flying from Peru
  for person in people:
    problem.addConstraint((
    lambda x,y:
    ((x == '2:30') and (y == 'peru')) or ((x != '2:30') and (y != 'peru'))    
    ), ['t_'+person, 'd_'+person])

  # The person flying from Yemen is leaving earlier than the person flying from Taiwan
  for person in people:
    for person2 in people:
      problem.addConstraint((
      lambda x,y,x2,y2:
      ((y == 'yemen' and y2 == 'taiwan') and (int)(x[0]) < (int)(x2[0])) or (y != 'yemen' or y2 != 'taiwan')
      ), ['t_'+person, 'd_'+person, 't_'+person2, 'd_'+person2])
  
  # The four travellers are Pablo, the traveller flying from Yemen, the person leaving at 2:30 pm
  # and the person leaving at 3:30 pm
  for person in people:
    if(person != 'pablo'):
      problem.addConstraint((
      lambda x,y:
      y == 'yemen' or x == '2:30' or x == '3:30'
      ), ['t_'+person, 'd_'+person])
    else:
      problem.addConstraint((
      lambda x,y:
      y != 'yemen' and x != '2:30' and x != '3:30'
      ), ['t_'+person, 'd_'+person])
  # implementing pairlist
  if(len(pairList)>0):
    for tuple in pairList:
      person = tuple[0]
      if((tuple[1].find(':30') != -1)):
        problem.addConstraint((
          lambda y:
          (y == tuple[1])
          ),['t_'+person])
      else:
        problem.addConstraint((
          lambda y:
          (y == tuple[1])
          ),['d_'+person])

  return problem.getSolutions()


# Task 2
def CommonSum(n):
  return (n*n*(n*n + 1)) / (2*n)


from constraint import *
# Task 3
def MSquares(n, pairList):
  sum = CommonSum(n)
  # print(sum)
  problem = constraint.Problem()
  problem.addVariables(range(0, n*n), range(1, n*n + 1))
  problem.addConstraint(constraint.AllDifferentConstraint(), range(0, n*n))
  if(len(pairList) > 0):
    for tuple in pairList:
      problem.addConstraint(constraint.ExactSumConstraint(tuple[1]), [tuple[0]])
  problem.addConstraint(constraint.ExactSumConstraint(sum), [i*(n+1) for i in range(n)])
  problem.addConstraint(constraint.ExactSumConstraint(sum), [(n*n-1)-((n-1)*(i+1)) for i in range(n)])
  for row in range(n):
    problem.addConstraint(constraint.ExactSumConstraint(sum),
    [row * n + i for i in range(n)])
  for col in range(n):
    problem.addConstraint(constraint.ExactSumConstraint(sum),
    [col + n * i for i in range(n)])
  
  
  solutions = problem.getSolutions()
  return solutions


# Task 4
def PMSquares(n, pairList):
  sum = CommonSum(n)
  # print(sum)
  problem = constraint.Problem()
  problem.addVariables(range(0, n*n), range(1, n*n + 1))
  problem.addConstraint(constraint.AllDifferentConstraint(), range(0, n*n))
  if(len(pairList) > 0):
    for tuple in pairList:
      problem.addConstraint(constraint.ExactSumConstraint(tuple[1]), [tuple[0]])
  problem.addConstraint(constraint.ExactSumConstraint(sum), [i*(n+1) for i in range(n)])
  problem.addConstraint(constraint.ExactSumConstraint(sum), [(n*n-1)-((n-1)*(i+1)) for i in range(n)])
  for row in range(n):
    problem.addConstraint(constraint.ExactSumConstraint(sum),
    [row * n + i for i in range(n)])
  for col in range(n):
    problem.addConstraint(constraint.ExactSumConstraint(sum),
    [col + n * i for i in range(n)])
  
  for i in range(1,n):
    x = 0; y = i
    bds = []
    for j in range(0,n):
      bds.append((x,y))
      x = (x+1)%n; y = (y+1)%n
    problem.addConstraint(constraint.ExactSumConstraint(sum),
                           [bds[i][0]*n + bds[i][1] for i in range(len(bds))])
    

  for i in range(0,n-1):
    x = 0; y = i
    bds = []
    for j in range(0,n):
      bds.append((x,y))
      x = (x+1)%n; y = (y-1+n)%n
    problem.addConstraint(constraint.ExactSumConstraint(sum),
                           [bds[i][0]*n + bds[i][1] for i in range(len(bds))])

  return problem.getSolutions()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# debug run
if __name__ == '__main__':
  if len(sys.argv) > 2:
    cmd = "{}({})".format(sys.argv[1], ",".join(sys.argv[2:]))
    print("debug run:", cmd)
    ret = eval(cmd)
    print("ret value:", ret)
    try:
      cnt = len(ret)
      print("ret count:", cnt)
    except TypeError:
      pass
  else:
    sys.stderr.write("Usage: {} <FUNCTION> <ARG>...\n".format(sys.argv[0]))
    sys.exit(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et ts=2 sw=2:
