import sys
import os
import pathlib
from typing import Union, Optional
import json_stream
from json_stream import streamable_list
import re
from time import time
from dataclasses import dataclass
from urllib.parse import urlparse
from enum import Enum
import json

class States(Enum):
  NEW_YORK = 39

def file_exists(p: pathlib.Path) -> Union[bool, Exception]:
  if os.path.exists(p) is True:
    return True
  else:
    raise Exception("Missing Index File!")

@dataclass
class InNetworkFile:
    """Class to store an In Network File record."""
    description: str
    location: str

    IN_NETWORK_FILES = "In-Network Negotiated Rates Files"

    def isInNetwork(self) -> bool:
      """Determine if the file is an In Network Rate file"""
      return self.description == self.IN_NETWORK_FILES
    
    def getInNetworkState(self) -> Optional[States]:
      """Parse `location` to return the state of the in Network file"""
      if not self.isInNetwork():
        return None

      url = urlparse(self.location)
      matches = re.findall(r"([0-9]{2}[a-zA-Z]{1}[0-9]{1})", url.path)

      if len(matches) == 1:
        state_num = int(matches[0][0:2])
        try:
          return States(state_num)
        except:
          return None
      else:
        return None

    def stateFilter(self, state_filter: States) -> bool:
      """Method to evaluate if a URL relates to a given state."""
      state = self.getInNetworkState()
      return state == state_filter
    
@streamable_list
def processStateInNetworkFiles(data, state: States):
  """Function to process the input data stream from the index file."""
  cnt = 0
  for r in data["reporting_structure"]:
    try:
      # This key is not required and thus must be checked.
      d = r["in_network_files"]
    except KeyError:
      continue

    for i in d:
      f = InNetworkFile(i["description"], i["location"])

      # Only process In Network Files
      if not f.isInNetwork():
        continue
      
      # Only process desired state In Network Files
      if not f.stateFilter(state):
        continue

      cnt += 1
      if cnt % 10000 == 0:
        print(str(cnt) + " Files Found.")

      yield f.location

def main():
  # Takes a single argument, the location of the index file.
  index_file = pathlib.Path(sys.argv[1])
  state = States.NEW_YORK

  #strt = time()
  if file_exists(index_file):
    with open(index_file, "r") as idxFile:
      with open("output/" + state.name + '.json', 'w', encoding='utf-8') as outFile:
        data = json_stream.load(idxFile)
        d = processStateInNetworkFiles(data, state)
        json.dump(d, outFile, indent=2)
  
  #end = time()
  #elapsed = end - strt
  #print("Elapsed: " + elapsed / 60 + " Mintures")
      
if __name__ == '__main__':
  main()
