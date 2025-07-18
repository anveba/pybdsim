import gzip as _gzip
"""
Module containing a similarly named Beam class for creating
a BDSIM beam distribution programmatically.
"""

BDSIMDistributionTypes = [
    'reference',
    'gaussmatrix',
    'gauss',
    'gausstwiss',
    'circle',
    'square',
    'ring',
    'eshell',
    'halo',
    'composite',
    'userfile',
    'ptc',
    'sixtrack',
    'eventgeneratorfile',
    'sphere',
    'compositesde',
    'box',
    'bdsimsampler',
    'halosigma'
]

BDSIMParticleTypes = [
    'e-',
    'e+',
    'proton',
    'gamma',
    'antiproton',
    'pi+',
    'pi-',
    'neutron',
    'photon',
    'mu+',
    'mu-',
    'kaon-',
    'kaon+',
    'kaon0L'
]

def WriteUserFile(filename, coordinates):
    """
    Function to write a BDSIM beamfile of type userfile.

    :param filename: Name of file to write the coordinates to
    :type filename: str
    :param coordinates: Coordinates of the different beam particles
    :type coordinates: list of list of float
    """
    compressed = filename.endswith(".gz")
    if compressed:
        f = _gzip.open(filename, 'wb')
    else:
        f = open(filename, 'w')

    def write(fn, s):
        if compressed:
            fn.write(s.encode('ascii'))
        else:
            fn.write(s)

    for n_coord, coord in enumerate(coordinates):
        s = ''
        for n_c, c in enumerate(coord):
            if n_c < len(coord) - 1  and n_coord <= len(coordinates) - 1:
                add = '\t'
            elif n_c == len(coord) - 1 and n_coord < len(coordinates) - 1:
                add = '\n'
            elif n_c == len(coord) - 1 and n_coord == len(coordinates) - 1:
                add = ''
            s += str(c) + add
        write(f, s)

    f.close()


class Beam(dict) :
    def __init__(self, particleType='e-', energy=1.0, distrType='reference', *args, **kwargs):
        dict.__init__(self,*args,**kwargs)
        self.SetParticleType(particleType)
        self.SetEnergy(energy)
        self.SetDistributionType(distrType)
        
    def SetParticleType(self,particleType='e-'):
        if particleType not in BDSIMParticleTypes:
            raise ValueError("Unknown particle type: '"+str(particleType)+"'")
        self['particle'] = '"' + str(particleType) + '"'

    def SetEnergy(self,energy=1.0,unitsstring='GeV'):
        self['energy'] = str(energy) + '*' + unitsstring

    def _MakeGaussTwiss(self):
        setattr(self, 'SetBetaX',      self._SetBetaX)
        setattr(self, 'SetBetaY',      self._SetBetaY)
        setattr(self, 'SetAlphaX',     self._SetAlphaX)
        setattr(self, 'SetAlphaY',     self._SetAlphaY)
        setattr(self, 'SetEmittanceX', self._SetEmittanceX)
        setattr(self, 'SetEmittanceY', self._SetEmittanceY)
        setattr(self, 'SetEmittanceNX', self._SetEmittanceNX)
        setattr(self, 'SetEmittanceNY', self._SetEmittanceNY)
        setattr(self, 'SetSigmaE',     self._SetSigmaE)
        setattr(self, 'SetSigmaT',     self._SetSigmaT)
        setattr(self, 'SetDispX',      self._SetDispX)
        setattr(self, 'SetDispY',      self._SetDispY)
        setattr(self, 'SetDispXP',     self._SetDispXP)
        setattr(self, 'SetDispYP',     self._SetDispYP)

    def SetDistributionType(self,distrType='reference'):
        if distrType not in BDSIMDistributionTypes:
            raise ValueError("Unknown distribution type: '"+str(distrType)+"'")
        self['distrType'] = '"' + distrType + '"'
        self._UpdateMemberFunctions(distrType)

    def __repr__(self):
        return self.ReturnBeamString()

    def _UpdateMemberFunctions(self, distrType):
        if distrType == 'reference':
            pass
        elif distrType == 'gaussmatrix':
            setattr(self, 'SegSigmaNM',    self._SetSigmaNM)
        elif distrType == 'gauss':
            setattr(self, 'SetSigmaX',     self._SetSigmaX)
            setattr(self, 'SetSigmaY',     self._SetSigmaY)
            setattr(self, 'SetSigmaE',     self._SetSigmaE)
            setattr(self, 'SetSigmaXP',    self._SetSigmaXP)
            setattr(self, 'SetSigmaYP',    self._SetSigmaYP)
            setattr(self, 'SetSigmaT',     self._SetSigmaT)   
        elif distrType == 'gausstwiss':
            self._MakeGaussTwiss()
        elif distrType == 'circle':
            setattr(self, 'SetEnvelopeR',  self._SetEnvelopeR)
            setattr(self, 'SetEnvelopeRp', self._SetEnvelopeRp)
            setattr(self, 'SetEnvelopeT',  self._SetEnvelopeT)
            setattr(self, 'SetEnvelopeE',  self._SetEnvelopeE)
        elif distrType == 'square':
            setattr(self, 'SetEnvelopeX',  self._SetEnvelopeX)
            setattr(self, 'SetEnvelopeXp', self._SetEnvelopeXp)
            setattr(self, 'SetEnvelopeY',  self._SetEnvelopeY)
            setattr(self, 'SetEnvelopeYp', self._SetEnvelopeYp)
            setattr(self, 'SetEnvelopeT',  self._SetEnvelopeT)
            setattr(self, 'SetEnvelopeE',  self._SetEnvelopeE)
        elif distrType == 'ring':
            setattr(self, 'SetRMin',       self._SetRMin)
            setattr(self, 'SetRMax',       self._SetRMax)
        elif distrType == 'eshell':
            setattr(self, 'SetShellX',     self._SetShellX)
            setattr(self, 'SetShellY',     self._SetShellY)
            setattr(self, 'SetShellXP',    self._SetShellXP)
            setattr(self, 'SetShellYP',    self._SetShellYP)
        elif distrType == 'halo':
            self._MakeGaussTwiss()
            setattr(self, 'SetHaloNSigmaXInner',      self._SetHaloNSigmaXInner)
            setattr(self, 'SetHaloNSigmaXOuter',      self._SetHaloNSigmaXOuter)
            setattr(self, 'SetHaloNSigmaYInner',      self._SetHaloNSigmaYInner)
            setattr(self, 'SetHaloNSigmaYOuter',      self._SetHaloNSigmaYOuter)
            setattr(self, 'SetHaloPSWeightParameter', self._SetHaloPSWeightParameter)
            setattr(self, 'SetHaloPSWeightFunction',  self._SetHaloPSWeightFunction)
            setattr(self, 'SetHaloXCutInner',         self._SetHaloXCutInner)
            setattr(self, 'SetHaloYCutInner',         self._SetHaloYCutInner)
        elif distrType == 'composite':
            setattr(self, 'SetXDistrType', self._SetXDistrType)
            setattr(self, 'SetYDistrType', self._SetYDistrType)
            setattr(self, 'SetZDistrType', self._SetZDistrType)
        elif distrType == 'ptc' : 
            setattr(self, 'SetSigmaE',     self._SetSigmaE)            
            setattr(self, 'SetDistribFileName',self._SetDistribFileName)
        elif distrType == "userfile":
            setattr(self, 'SetDistrFile',     self._SetDistrFile)
            setattr(self, 'SetDistrFileFormat',self._SetDistrFileFormat)

    def WriteToFile(self, filename):
        f = open(filename, 'w')
        f.write(self.ReturnBeamString())
        f.close()
            
    def ReturnBeamString(self):
        s = ''
        for k,v in sorted(self.items()):
            s += ', \n\t'+str(k)+'='+str(v)
        s += ';'
        s2 = s.split('\n')
        s3 = 'beam,\t'+s2[1].replace('\t','').replace('\n','').replace(',','').strip()+',\n'
        s4 = '\n'.join(s2[2:])
        st = s3+s4
        return st

    def SetX0(self,x0=0.0,unitsstring='m'):
        self['X0'] = str(x0) + '*' + unitsstring

    def SetY0(self,y0=0.0,unitsstring='m'):
        self['Y0'] = str(y0) + '*' + unitsstring

    def SetZ0(self,z0=0.0,unitsstring='m'):
        self['Z0'] = str(z0) + '*' + unitsstring

    def SetXP0(self,xp0=0.0):
        self['Xp0'] = str(xp0)

    def SetYP0(self,yp0=0.0):
        self['Yp0'] = str(yp0)

    def SetZP0(self,zp0=0.0):
        self['Zp0'] = str(zp0)

    def SetS0(self, s0=0,unitsstring='m'):
        self['S0'] = str(s0) + '*' + unitsstring

    def SetE0(self, e0=1, unitsstring='GeV'):
        self['E0'] = str(e0) + '*' + unitsstring

    def SetT0(self,t0=0.0,unitsstring='s'):
        self['T0'] = str(t0) + '*' + unitsstring

    def _SetSigmaNM(self, n, m, value):
        self['sigma'+str(n)+str(m)] = value

    def _SetSigmaX(self,sigmax=1.0,unitsstring='um'):
        self['sigmaX'] = str(sigmax) + '*' + unitsstring

    def _SetSigmaY(self,sigmay=1.0,unitsstring='um'):
        self['sigmaY'] = str(sigmay) + '*' + unitsstring

    def _SetSigmaE(self,sigmae=0.001):
        """
        fractional energy spread
        """
        self['sigmaE'] = str(sigmae)

    def _SetSigmaXP(self,sigmaxp=1.0,unitsstring='mrad'):
        self['sigmaXp'] = str(sigmaxp) + '*' + unitsstring

    def _SetSigmaYP(self,sigmayp=1.0,unitsstring='mrad'):
        self['sigmaYp'] = str(sigmayp) + '*' + unitsstring

    def _SetSigmaT(self,sigmat=1.0,unitsstring='s'):
        self['sigmaT'] = str(sigmat)

    def _SetBetaX(self, betx=1.0, unitsstring='m'):
        self['betx'] = str(betx) + '*' + unitsstring

    def _SetBetaY(self,bety=1.0,unitsstring='m'):
        self['bety'] = str(bety) + '*' + unitsstring

    def _SetAlphaX(self,alphax=1.0,unitsstring='m'):
        self['alfx'] = str(alphax)

    def _SetAlphaY(self,alphay=1.0,unitsstring='m'):
        self['alfy'] = str(alphay)

    def _SetDispX(self,dispx=1.0,unitsstring='m'):
        self['dispx'] = str(dispx) + '*' + unitsstring

    def _SetDispY(self,dispy=1.0,unitsstring='m'):
        self['dispy'] = str(dispy) + '*' + unitsstring

    def _SetDispXP(self,dispxp=1.0):
        self['dispxp'] = str(dispxp)

    def _SetDispYP(self,dispyp=1.0):
        self['dispyp'] = str(dispyp)

    def _SetEmittanceX(self,emitx=1.0e-9,unitsstring='um'):
        self['emitx'] = str(emitx) + '*' + unitsstring
   
    def _SetEmittanceY(self,emity=1.0e-9,unitsstring='um'):
        self['emity'] = str(emity) + '*' + unitsstring

    def _SetEmittanceNX(self,emitnx=1.0e-9,unitsstring='mm*mrad'):
        self['emitnx'] = str(emitnx) + '*' + unitsstring

    def _SetEmittanceNY(self,emitny=1.0e-9,unitsstring='mm*mrad'):
        self['emitny'] = str(emitny) + '*' + unitsstring

    def _SetShellX(self,shellx=1.0,unitsstring='m'):
        self['shellX'] = str(shellx) + '*' + unitsstring

    def _SetShellY(self,shelly=1.0,unitsstring='m'):
        self['shellY'] = str(shelly) + '*' + unitsstring

    def _SetShellXP(self,shellxp=1.0):
        self['shellXp'] = str(shellxp)

    def _SetShellYP(self,shellyp=1.0):
        self['shellYp'] = str(shellyp)

    def _SetEnvelopeR(self, enveloper=1.0, unitsstring='um'):
        self['envelopeR'] = str(enveloper) + '*' + unitsstring

    def _SetEnvelopeRp(self, enveloperp=1.0, unitsstring='mrad'):
        self['envelopeRp'] = str(enveloperp) + '*' + unitsstring

    def _SetEnvelopeT(self, envelopet=1.0,unitsstring='s'):
        self['envelopeT'] = str(envelopet) + '*' + unitsstring

    def _SetEnvelopeE(self, envelopee=1.0,unitsstring='GeV'):
        self['envelopeE'] = str(envelopee) + '*' + unitsstring

    def _SetEnvelopeX(self, envelopex=1.0,unitsstring='m'):
        self['envelopeX'] = str(envelopex) + '*' + unitsstring

    def _SetEnvelopeY(self, envelopey=1.0,unitsstring='m'):
        self['envelopeY'] = str(envelopey) + '*' + unitsstring

    def _SetEnvelopeXp(self, envelopexp=1.0,unitsstring='mrad'):
        self['envelopeXp'] = str(envelopexp) + '*' + unitsstring

    def _SetEnvelopeYp(self, envelopeyp=1.0,unitsstring='mrad'):
        self['envelopeYp'] = str(envelopeyp) + '*' + unitsstring

    def _SetHaloNSigmaXInner(self, halonsigmaxinner=1):
        self['haloNSigmaXInner'] = str(halonsigmaxinner)

    def _SetHaloNSigmaXOuter(self, halonsigmaxouter=2):
        self['haloNSigmaXOuter'] = str(halonsigmaxouter)

    def _SetHaloNSigmaYInner(self, halonsigmayinner=1):
        self['haloNSigmaYInner'] = str(halonsigmayinner)

    def _SetHaloNSigmaYOuter(self, halonsigmayouter=2):
        self['haloNSigmaYOuter'] = str(halonsigmayouter)

    def _SetHaloPSWeightParameter(self, param):
        self['haloPSWeightParameter'] = param

    def _SetHaloPSWeightFunction(self, func):
        self['haloPSWeightFunction'] = '"'+func+'"'

    def _SetHaloXCutInner(self, haloxcutinner=0):
        self['haloXCutInner'] = str(haloxcutinner)

    def _SetHaloYCutInner(self, haloycutinner=0):
        self['haloYCutInner'] = str(haloycutinner)

    def _SetRMin(self,rmin=0.9,unitsstring='mm'):
        self['Rmin'] = str(rmin) + '*' + unitsstring
    
    def _SetRMax(self,rmax=1.0,unitsstring='mm'):
        self['Rmax'] = str(rmax) + '*' + unitsstring

    def _SetDistribFileName(self, fileName) :
        self['distrFile'] = '"'+fileName+'"'

    def _SetXDistrType(self, name):
        self._UpdateMemberFunctions(name)
        self['xDistrType'] = '"' + name + '"'

    def _SetYDistrType(self, name):
        self._UpdateMemberFunctions(name)
        self['yDistrType'] = '"' + name + '"'

    def _SetZDistrType(self, name):
        self._UpdateMemberFunctions(name)
        self['zDistrType'] = '"' + name + '"'

    def _SetOffsetSampleMean(self,on=False):
        if on == True:
            self["offsetSampleMean"] = 1
        else:
            self["OffsetSampleMean"] = 0

    def _SetDistrFile(self, filename):
        self["distrFile"] = '"{}"'.format(filename)

    def _SetDistrFileFormat(self, format_string):
        self["distrFileFormat"] = '"{}"'.format(format_string)

    def _SetDistrFileLoop(self, loop=0):
        self["distrFileLoop"] = loop

    def _MakeGaussTwiss(self):
        setattr(self, 'SetBetaX',      self._SetBetaX)
        setattr(self, 'SetBetaY',      self._SetBetaY)
        setattr(self, 'SetAlphaX',     self._SetAlphaX)
        setattr(self, 'SetAlphaY',     self._SetAlphaY)
        setattr(self, 'SetEmittanceX', self._SetEmittanceX)
        setattr(self, 'SetEmittanceY', self._SetEmittanceY)
        setattr(self, 'SetEmittanceNX', self._SetEmittanceNX)
        setattr(self, 'SetEmittanceNY', self._SetEmittanceNY)
        setattr(self, 'SetSigmaE',     self._SetSigmaE)
        setattr(self, 'SetSigmaT',     self._SetSigmaT)
        setattr(self, 'SetDispX',      self._SetDispX)
        setattr(self, 'SetDispY',      self._SetDispY)
        setattr(self, 'SetDispXP',     self._SetDispXP)
        setattr(self, 'SetDispYP',     self._SetDispYP)
