import graph_index_repo
from graph_index_repo import graph_index_repo
import numpy

class mem_repo(graph_index_repo):
    
    adj_matrix: dict = {}
    uuidToCompressed: dict = {}
    compressedToUUID: dict = {}
    currentId = 0
    RADIX = 36

    def next( self ) :
        self.currentId += 1
        return numpy.base_repr( self.currentId, self.RADIX )

    def get(self, id: str ):
        if id in self.adj_matrix:
            return self.adj_matrix[id]
        return None
    
    def getCompressed( self, string: str) :
        result = self.uuidToCompressed.get( string )
        if result == None:
            result = self.next()
            self.uuidToCompressed[string] = result
            self.compressedToUUID[result] = string
        return result
    
    def index(self, source: str, dest: str, relationship: str):
        compressedSource = self.getCompressed( source )
        compressedDest = self.getCompressed( dest )
        val = compressedDest + ":" + relationship
        value = self.adj_matrix.get(compressedSource)
        if value is not None:
            value.append(val)
        else:
            value = [val]
        self.adj_matrix[compressedSource] = value

    def size(self):
        return len(self.adj_matrix)

def main() :
    print( "In the main method" )
    repo = mem_repo()
    for x in range( 1, 100 ) :
         #repo.index( x, x+1, 'rel' )
        print( x, repo.next() )
    #print( repo.adj_matrix )
    
     
if __name__ == '__main__' :
         main()