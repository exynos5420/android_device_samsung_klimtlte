#!/usr/bin/python

import hashlib
import re

# It seems that using the stock samsung values is to silent for aosp. Boost mic by 1.3
MIC_BOOST_FACTOR = 1.3

inoutMap = []
inputChannelMap = []
coreMap = []
deviceMap = []
verbMap = []
channelMap = []

def convertDeviceName(name):
  if name == "headphone":
    name = "headphones"
  elif name == "sco":
    name = "bt-sco"
  elif name == "analogue dock out":
    name = "analog-dock"
  elif name == "aux digital out":
    name = "aux-digital"

  elif name == "builtin mic":
    name = "main-mic"
  elif name == "back mic":
    name = "second-mic"
  elif name == "headset in":
    name = "headset-mic"
  elif name == "sco headset in":
    name = "bt-sco-mic"
  return name

class Element:
  key = ""
  value = ""
  valueOrg = ""

  def __str__(self, tab=2):
    value = self.value
    if self.valueOrg is not "":
      value = self.valueOrg

    try:
      valueI = int(value)
      valueS = str(valueI)
    except:
      valueS = "\"" + value + "\""
    return "\t"*tab + "{ \"" + self.key + "\", " + valueS + " },"

  def toMixerPaths(self, tab=2):
    return "  "*tab + "<ctl name=\"" + self.key + "\" value=\"" + self.value + "\" />"

class TinyUCMElement:
  typ = ""
  name = ""
  enable = []

  def __init__(self, typ, text):
    self.enable = []
    self.typ = typ
    try:
      self.name = re.findall(typ + " \"(.+)\" {", text)[0].lower()
    except:
      #print "Error on modifier"
      #print text
      return

    if self.typ == "ChannelSource":
      self.typ = "Channel"

    self.typ = self.typ.lower()
    enableStr = text[text.find("Enable {"):]
    if "Disable" in enableStr:
      enableStr = enableStr[:enableStr.find("Disable")]

    enableStr = re.findall("{(.+)}", enableStr)
    for enable in enableStr:
      enableSplit = enable.split(",")
      #print enableSplit
      e = Element()
      e.key = re.findall("\"(.+)\"", enableSplit[0])[0]
      try:
        e.value = re.findall("\"(.+)\"", enableSplit[1])[0]
      except:
        e.value = enableSplit[1].strip()

      self.enable.append(e)
      del e

    scenarioStr = text[text.find("Scenario \"default\" {"):]
    if len(scenarioStr) > 0:
      enableStr = scenarioStr[scenarioStr.find("Enable {"):]
      if "Scenario" in enableStr:
        enableStr = enableStr[:enableStr.find("Scenario")]

      enableStr = re.findall("{(.+)}", enableStr)
      for enable in enableStr:
        enableSplit = enable.split(",")
        #print enableSplit
        e = Element()
        e.key = re.findall("\"(.+)\"", enableSplit[0])[0]
        try:
          e.value = re.findall("\"(.+)\"", enableSplit[1])[0]
        except:
          e.value = enableSplit[1].strip()

        self.enable.append(e)
        del e
      #exit(0)

  def __str__(self):
    s = "    <!--\n"
    for e in self.enable:
      s += str(e) + "\n"
    s += "    -->"
    return s

  def toMixerPaths(self):
    s = ""
    if self.typ != "device":
      s += "  <path name=\"" + self.typ + "-" + self.name + "\">\n"

      s += str(self) + "\n"

    for e in self.enable:
      s += e.toMixerPaths() + "\n"

    if self.typ != "device":
      s += "  </path>"
    return s

class Gain:
  modifier = ""
  device = ""
  channel = ""
  enable = []

  UNKNOWN = 0
  OUTPUT = 1
  INPUT = 2

  deviceType = UNKNOWN

  def __init__(self, text):
    self.enable = []
    try:
      self.modifier = re.findall("Modifier \"(.+)\" {", text)[0].lower()
    except:
      #print "Error on modifier"
      #print text
      return

    try:
      self.device = re.findall("SupportedDevice {[\w\s]+\"(.+)\"", text)[0].lower()
    except:
      #print "Error on device"
      #print text
      return

    self.channel = "unknown"

    channelDevice = self.device
    #print channelDevice
    for cl in inoutMap:
      #print cl.key
      if cl.key == self.device:
        channelDevice = cl.value

    #print channelDevice
    for c in inputChannelMap:
      #print c.key
      if c.key == channelDevice:
        self.channel = c.value

    #print self.channel

    #exit(0)
    self.deviceOrg = self.device
    self.modifierOrg = self.modifier

    self.device = convertDeviceName(self.device)

    if self.device in ("speaker", "earpiece", "headphones", "bt-sco", "analog-dock", "aux-digital"):
      self.deviceType = self.OUTPUT
    elif self.device in ("main-mic", "second-mic", "headset-mic", "bt-sco-mic"):
      self.deviceType = self.INPUT
    else:
      self.deviceType = self.UNKNOWN

    if self.deviceType == self.INPUT and self.modifier == "voice":
      self.modifier = "voicecall"
    elif self.deviceType == self.INPUT and self.modifier == "recognition":
      self.modifier = "voice-rec"
    elif self.deviceType == self.OUTPUT and self.modifier == "incall":
      self.modifier = "voice"
    elif self.deviceType == self.OUTPUT and self.modifier == "incommunication":
      self.modifier = "communication"

    enableStr = re.findall("{(.+)}", text)
    for enable in enableStr:
      enableSplit = enable.split(",")
      e = Element()
      e.key = re.findall("\"(.+)\"", enableSplit[0])[0]
      e.value = enableSplit[1].strip()
      
      if self.deviceType == self.INPUT:
        if e.key in ("IN1R Volume", "IN1L Volume", "IN2R Volume", "IN2L Volume"):
          #print "OLD:", e.value
          e.valueOrg = e.value
          e.value = str(int (float(e.value) * MIC_BOOST_FACTOR))
          #print "NEW:", e.value
      
      self.enable.append(e)
      del e
  
  def __str__(self):
    s = "    <!--\n"
    for e in self.enable:
      s += str(e) + "\n"
    s += "    -->"
    return s

  def toMixerPaths(self, om=None):
    m = self.modifier
    if om is not None:
      m = om

    if m == "normal" or m == "voicecall":
      s = "  <path name=\"" + self.device + "\">\n"

      for device in deviceMap:
        if convertDeviceName(device.name) == self.device:
          s += str(device) + "\n"

      s += str(self) + "\n"
      if self.deviceType == self.INPUT and self.channel != "unknown":
        s += "    <path name=\"channel-" + self.channel + "\" />\n"
      s += "    <path name=\"verb-" + m + "\" />\n\n"

      for device in deviceMap:
        if convertDeviceName(device.name) == self.device:
          s += device.toMixerPaths() + "\n"

    else:
      s = "  <path name=\"" + m + "-" + self.device + "\">\n\n"
      s += str(self) + "\n"
      s += "    <path name=\"" + self.device + "\" />\n\n"

    for e in self.enable:
      s += e.toMixerPaths() + "\n"

    s += "  </path>"
    return s

def findGain(gains, device, modifier):
  for g in gains:
    if g.device == device and g.modifier == modifier:
      return g

  return None

fileTinyucm = open("tinyucm.conf", "r")
fileDefaultgain = open("default_gain.conf", "r")

tinyucm = fileTinyucm.read()
tinyucmElements = tinyucm.split("\n}")


for tinyucmElement in tinyucmElements:
  e = tinyucmElement.strip()

  #print e
  while e[:1] == "#" or e[:2] == "//":
    e = e.split('\n', 1)[1]
    #print e
    #exit(0)

  if "INOUT_MAP" in e:
    e = "INOUT_MAP" + e.split("INOUT_MAP")[1]

  if e.startswith("INOUT_MAP"):
    enableStr = re.findall("{(.+)}", e)
    for enable in enableStr:
      enableSplit = enable.split(",")
      e = Element()
      e.key = re.findall("\"(.+)\"", enableSplit[0])[0].lower()
      e.value = re.findall("\"(.+)\"", enableSplit[1])[0].lower()
      inoutMap.append(e)
      del e

    #for cl in inoutMap:
    #  print cl

  elif e.startswith("INPUT_CHANNEL_MAP"):
    enableStr = re.findall("{(.+)}", e)
    for enable in enableStr:
      enableSplit = enable.split(",")
      e = Element()
      e.key = re.findall("\"(.+)\"", enableSplit[0])[0].lower()
      e.value = re.findall("\"(.+)\"", enableSplit[1])[0].lower()
      inputChannelMap.append(e)
      del e

  elif e.startswith("Core"):
    enableStr = re.findall("{(.+)}", e)
    for enable in enableStr:
      enableSplit = enable.split(",")
      e = Element()
      e.key = re.findall("\"(.+)\"", enableSplit[0])[0]
      k = re.findall("\"(.+)\"", enableSplit[1])
      if len(k) == 0:
        e.value = enableSplit[1].strip()
      else:
        e.value = k[0].strip()

      #Even if tinymix sets 0, we need 130Hz!
      if e.key == "LHPF1 COEFF FILTER" or e.key == "LHPF2 COEFF FILTER":
        e.value = "130Hz"

      coreMap.append(e)
      del e

  elif e.startswith("ChannelSource"):
    t = TinyUCMElement("ChannelSource", e)
    channelMap.append(t);
    #print t
    #exit(0)

  elif e.startswith("Verb"):
    t = TinyUCMElement("Verb", e)
    if t.name in ("normal", "voicecall"):
      verbMap.append(t);
    #exit(0)


  elif e.startswith("Device"):
    t = TinyUCMElement("Device", e)
    deviceMap.append(t);
    #exit(0)

#print inputChannelMap

#channelmap = re.findall("INPUT_CHANNEL_MAP {[\w\s]+(.*)", tinyucm)
#print channelmap


#print re.findall("{(.+)}", tinyucm)

defaultGain = fileDefaultgain.read()

defaultGainElements = defaultGain.split("\n}")
gains = []
for gainElement in defaultGainElements:
  g = Gain(gainElement)

  if g.deviceType == Gain.OUTPUT:
    if g.modifier in ("normal", "voice", "communication"):
      gains.append(g)

  if g.deviceType == Gain.INPUT:
    if g.modifier in ("voicecall", "voice-rec", "communication"):
      gains.append(g)

#for g in gains:
#  print g.toMixerPaths()

print """<mixer>
"""
print "  <!-- file automatically generated by tinyucm2mixerpaths.py (C) 2016 Schischu -->"
print "  <!-- default_gain.conf: " + hashlib.md5(open("default_gain.conf", 'rb').read()).hexdigest() + " -->"
print "  <!-- tinyucm.conf: " + hashlib.md5(open("tinyucm.conf", 'rb').read()).hexdigest() + " -->"

print"""
  <!-- Initial mixer settings -->"""

for c in coreMap:
  print c.toMixerPaths(1)

print """
  <!-- Channels -->"""

for c in channelMap:
  print c.toMixerPaths() + "\n"

print """
  <!-- Verbs -->"""

for v in verbMap:
  print v.toMixerPaths() + "\n"

print """<!-- Paths that roughly correspond to devices -->"""

print findGain(gains, "speaker", "normal").toMixerPaths() + "\n"
print findGain(gains, "earpiece", "normal").toMixerPaths() + "\n"
print findGain(gains, "headphones", "normal").toMixerPaths() + "\n"
print findGain(gains, "bt-sco", "normal").toMixerPaths()

print """
  <path name="bt-sco-headset">
      <path name="bt-sco" />
  </path>

  <path name="bt-sco-carkit">
      <path name="bt-sco" />
  </path>
"""
print findGain(gains, "analog-dock", "normal").toMixerPaths() + "\n"
print findGain(gains, "aux-digital", "normal").toMixerPaths() + "\n"

print findGain(gains, "main-mic", "voicecall").toMixerPaths()
print """
  <path name="builtin-mic">
    <path name="main-mic" />
  </path>
"""
print findGain(gains, "second-mic", "voicecall").toMixerPaths()
print """
  <path name="back-mic">
      <path name="second-mic" />
  </path>
"""
print findGain(gains, "headset-mic", "voicecall").toMixerPaths() + "\n"
print findGain(gains, "bt-sco-mic", "voicecall").toMixerPaths()

print """
  <!-- Abstract devices -->

  <path name="speaker-and-headphones">
      <path name="speaker" />
      <path name="headphones" />
  </path>
"""
print """
  <!-- Playback paths Normal/Voice-->
  <path name="media-speaker">
    <path name="speaker" />
  </path>

  <path name="media-earpiece">
    <path name="earpiece" />
  </path>

  <path name="media-headphones">
    <path name="headphones" />
  </path>

  <path name="media-main-mic">
      <path name="main-mic" />
  </path>

  <path name="media-second-mic">
      <path name="main-mic" />
  </path>

  <path name="media-headset-mic">
      <path name="headset-mic" />
  </path>
"""

print """
  <!-- Playback paths InCall/Voice -->
"""
print findGain(gains, "speaker", "voice").toMixerPaths() + "\n"
print findGain(gains, "earpiece", "voice").toMixerPaths() + "\n"
print findGain(gains, "headphones", "voice").toMixerPaths() + "\n"
print findGain(gains, "bt-sco", "voice").toMixerPaths() + "\n"

print findGain(gains, "main-mic", "voicecall").toMixerPaths(om="voice") + "\n"
print findGain(gains, "second-mic", "voicecall").toMixerPaths(om="voice") + "\n"
print findGain(gains, "headset-mic", "voicecall").toMixerPaths(om="voice") + "\n"
print findGain(gains, "bt-sco-mic", "voicecall").toMixerPaths(om="voice")

print """
  <!-- Playback paths Normal/Recognition-->
  <path name="voice-rec-speaker">
    <path name="speaker" />
  </path>

  <path name="voice-rec-headphones">
    <path name="headphones" />
  </path>
"""
print findGain(gains, "main-mic", "voice-rec").toMixerPaths() + "\n"
print findGain(gains, "second-mic", "voice-rec").toMixerPaths() + "\n"
print findGain(gains, "headset-mic", "voice-rec").toMixerPaths()
print """
  <path name="voice-rec-bt-sco-mic">
    <!--
    -->
      <path name="bt-sco-mic" />
  </path>
"""

print """
  <!-- Playback paths Incommunication/Communication -->
"""
print findGain(gains, "speaker", "communication").toMixerPaths() + "\n"
print findGain(gains, "earpiece", "communication").toMixerPaths() + "\n"
print findGain(gains, "headphones", "communication").toMixerPaths() + "\n"
print findGain(gains, "bt-sco", "communication").toMixerPaths() + "\n"

print findGain(gains, "main-mic", "communication").toMixerPaths() + "\n"
print findGain(gains, "second-mic", "communication").toMixerPaths() + "\n"
print findGain(gains, "headset-mic", "communication").toMixerPaths()

print """

  <path name="communication-bt-sco-mic">
    <!--
    -->
      <path name="bt-sco-mic" />
  </path>

  <path name="none">
      <!-- Empty path -->
  </path>

</mixer>"""
