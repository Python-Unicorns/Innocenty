__author__ = 'rabbiabram@gmail.com'

from server import gossip
from random import randint
import sys
import getopt

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hopm:v", ["help", "output=", 'port=', 'master-port='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        #usage()
        sys.exit(2)
    output = None
    verbose = False
    port = None
    master_port = None
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-p", "--port"):
            port = a
        elif o in ('-m', "--master-port"):
            master_port = a
        elif o in ("-h", "--help"):
            #usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    # if (port is None or master_port is None):
    #     sys.exit(1)
    # else:
    print(port, master_port)
    node = gossip.GossipSocket(name=port, port=port)
    if (master_port is not None):
        node.add_master(master_port)
    node.sstart()

if __name__ == "__main__":
    main()