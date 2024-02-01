from controllers import *
import os

if __name__ == '__main__':
    port:int=int(os.environ.get('PORT',8080))
    app.run(debug=True,host='0.0.0.0',port=8080)
    
    