## Pysumi ##
### A Python interface for Apple's [Find My iPhone](http://www.apple.com/mobileme/features/find-my-iphone.html) service ###

#### Where does the name come from? ####
Pysumi gets its name from [sosumi](https://github.com/tylerhall/sosumi) a php and cocoa wrapper around Apple's undocumented Find My iPhone api, which as far as I know was the first wrapper. Related projects include [node-sosumi](https://github.com/drudge/node-sosumi) (a javascript/node js wrapper) and [rosumi](https://github.com/hpop/rosumi) (a ruby wrapper).

#### How do I use this? ####
    # Create the Pysumi object
    from pysumi import Pysumi
    findphone = Pysumi(mobilemeemail, mobilemepassword)
    
    # Update findphone.devices list with location and other data for devices
    findphone.updateDevices()
    
    # Send a message to a device
    findphone.sendMessage(device from devices list,"Subject","Message")
    
    # Remote lock a device
    findphone.lockDevice(device from devices list, 4-digit lock code)

#### License ####
The MIT License

Copyright (c) 2010 Michael Weisman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.