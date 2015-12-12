import FWCore.ParameterSet.Config as cms

#process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
'''
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
'''
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

# --------------------- GlobalTag ----------------------
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '') 
# auto:run2_mc = 'MCRUN2_74_V7'
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')
#print process.GlobalTag.globaltag
import CalibTracker.Configuration.Common.PoolDBESSource_cfi

# ---------------------- PB Geometry -------------------
process.trackerGeometryDB.applyAlignment = cms.bool(False)
process.XMLFromDBSource.label=''
process.PoolDBESSourceGeometry = cms.ESSource("PoolDBESSource",
	process.CondDBSetup,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(
		cms.PSet(
			record = cms.string('GeometryFileRcd'),
			tag = cms.string('XMLFILE_Geometry_74YV2_Extended2015_mc')
		),
		cms.PSet(
			record = cms.string('IdealGeometryRecord'),
			tag = cms.string('TKRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PGeometricDetExtraRcd'),
			tag = cms.string('TKExtra_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PTrackerParametersRcd'),
			tag = cms.string('TKParameters_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalBarrelRcd'),
			tag = cms.string('EBRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalEndcapRcd'),
			tag = cms.string('EERECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalPreshowerRcd'),
			tag = cms.string('EPRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PHcalRcd'),
			tag = cms.string('HCALRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PCaloTowerRcd'),
			tag = cms.string('CTRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PZdcRcd'),
			tag = cms.string('ZDCRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PCastorRcd'),
			tag = cms.string('CASTORRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('CSCRecoGeometryRcd'),
			tag = cms.string('CSCRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('CSCRecoDigiParametersRcd'),
			tag = cms.string('CSCRECODIGI_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('DTRecoGeometryRcd'),
			tag = cms.string('DTRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('RPCRecoGeometryRcd'),
			tag = cms.string('RPCRECO_Geometry_74YV2')
		)
	),
	connect = cms.string('sqlite_file:./DBs/PilotGeometry.db') 
		#PilotGeometry.db --> with PB and Fake PB
		#PilotGeometry0.db --> with PB only
)
process.es_prefer_geometry = cms.ESPrefer( "PoolDBESSource", "PoolDBESSourceGeometry" )
#-------------------------------------------------------

# --------------------- SiPixelQuality -----------------
process.SiPixelQualityDBReader = cms.ESSource("PoolDBESSource",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
	    messageLevel = cms.untracked.int32(0),
	    authenticationPath = cms.untracked.string('')
	),
	connect = cms.string ('sqlite_file:./DBs/SiPixelQuality_PilotBlade4.db'), 
		#Fake Pilot Blade out, Pilot Blade in --> PilotBlade3.db
		#Fake Pilot Blade out, Pilot Blade out --> PilotBlade4.db
    toGet = cms.VPSet(
    	cms.PSet(
			record = cms.string('SiPixelQualityFromDbRcd'),
			tag = cms.string('SiPixelQuality_PilotBlade')
        )
    )
)
process.es_prefer_Quality = cms.ESPrefer("PoolDBESSource","SiPixelQualityDBReader")
#-------------------------------------------------------


# --------------------- CablingMap ---------------------
process.CablingMapDBReader = cms.ESSource("PoolDBESSource",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
	    messageLevel = cms.untracked.int32(0),
	    authenticationPath = cms.untracked.string('')
	),
	connect = cms.string('sqlite_file:./DBs/SiPixelCabling_PilotBlade.db'), 
		#SiPixelCabling_Ph0andPilotBlade.db --> PB + BPix + FPix
		#SiPixelCabling_PilotBlade.db --> just PB, no BPix, no FPix
    toGet = cms.VPSet(
    	cms.PSet(
		    record = cms.string('SiPixelFedCablingMapRcd'),
			label = cms.untracked.string('pilotBlade'), 
        	tag = cms.string('SiPixelFedCablingMap_mc')
    	)
    )
)
process.es_prefer_CablingReader = cms.ESPrefer("PoolDBESSource","CablingMapDBReader")
#-------------------------------------------------------

# --------------------- Gain Calab DB ------------------
process.GainDBReader = cms.ESSource("PoolDBESSource",
        BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0),
            authenticationPath = cms.untracked.string('')
        ),
        connect = cms.string ('sqlite_file:./DBs/GainDB_PilotBlade.db'),
    toGet = cms.VPSet(
        cms.PSet(
                        record = cms.string('SiPixelGainCalibrationOfflineRcd'),
                        tag = cms.string('GainCalib_TEST_offline')
        )
    )
)
process.es_prefer_Gain = cms.ESPrefer("PoolDBESSource","GainDBReader")
#-------------------------------------------------------

# --------------------- LorentzAngle -------------------

process.LorentzAngleDBReader = cms.ESSource("PoolDBESSource",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
	    messageLevel = cms.untracked.int32(0),
	    authenticationPath = cms.untracked.string('')
	),
	connect = cms.string ('sqlite_file:./DBs/SiPixelLorentzAngle_PilotBlade3.db'),
    toGet = cms.VPSet(
      	cms.PSet(
			record = cms.string('SiPixelLorentzAngleRcd'),
			label = cms.untracked.string(''),
                        tag = cms.string('SiPixelLorentzAngle_v02_mc')
		),
	),
)
process.es_prefer_LA = cms.ESPrefer("PoolDBESSource","LorentzAngleDBReader")

# forWidth LA
process.LAWidthReader = cms.ESSource("PoolDBESSource",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
	    messageLevel = cms.untracked.int32(0),
	    authenticationPath = cms.untracked.string('')
	),
	#connect = cms.string ('sqlite_file:./DBs/SiPixelLorentzAngle_PilotBlade4.db'),
	connect = cms.string ('sqlite_file:./DBs/SiPixelLorentzAngle_PilotBlade5.db'),
    toGet = cms.VPSet(
      	cms.PSet(
			record = cms.string('SiPixelLorentzAngleRcd'),
			label = cms.untracked.string('forWidth'),
                        #tag = cms.string('SiPixelLorentzAngle_forWidth_v1_mc')
                        tag = cms.string('SiPixelLorentzAngle_forWidth_v1_mc[cms_orcon_prod/CMS_COND_31X_PIXEL]')
		),
	),
)
process.es_prefer_LAWidth = cms.ESPrefer("PoolDBESSource","LAWidthReader")
# fromAlignment LA
process.LAAlignmentReader = cms.ESSource("PoolDBESSource",
        BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0),
            authenticationPath = cms.untracked.string('')
        ),
        #connect = cms.string ('sqlite_file:./DBs/SiPixelLorentzAngle_PilotBlade4.db'),
        connect = cms.string ('sqlite_file:./DBs/SiPixelLorentzAngle_PilotBlade6.db'),
    toGet = cms.VPSet(
        cms.PSet(
                        record = cms.string('SiPixelLorentzAngleRcd'),
                        label = cms.untracked.string('fromAlignment'),
                        #tag = cms.string('SiPixelLorentzAngle_forWidth_v1_mc')
                        tag = cms.string('SiPixelLorentzAngle_fromAlignment_v1_mc[cms_orcon_prod/CMS_COND_31X_PIXEL]')
                ),
        ),
)
process.es_prefer_LAAlignment = cms.ESPrefer("PoolDBESSource","LAAlignmentReader")
#-------------------------------------------------------

# ----------------------- GenError ---------------------
process.GenErrReader = cms.ESSource("PoolDBESSource",
	DBParameters = cms.PSet(
		messageLevel = cms.untracked.int32(0),
		authenticationPath = cms.untracked.string('')
	),
	toGet = cms.VPSet(
		cms.PSet(
			record = cms.string('SiPixelGenErrorDBObjectRcd'),
			tag = cms.string('SiPixelGenErrorDBObject38T3')
		),
	),
	connect = cms.string('sqlite_file:./DBs/SiPixelGenErrors38T3_PilotBlade.db')
)
process.es_prefer_GenErr = cms.ESPrefer("PoolDBESSource","GenErrReader")
#-------------------------------------------------------
'''
process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('PilotMinBias_13TeV_cfi_py_RAW2DIGI_L1Reco_RECO'+nEvents+'.root'),
    outputCommands = cms.untracked.vstring(
    'drop *',
    'keep *_*ixel*_*_*',
    'keep *_*ip*_*_*',
    'keep *_*PB*_*_*',
    'keep *_*generalTracks*_*_*',
    'keep *_*eamSpot*_*_*',
    'keep *ileupSummaryInfo_*_*_*',
    'keep *_*onditions*_*_*',
    
    ),
    splitLevel = cms.untracked.int32(0)
)

# --------------------- Reconstruction --------------------
#Standard Digis
# standard CablingMap does not contain PB FEDs --> no siPixelDigis
process.siPixelDigis.UsePilotBlade = cms.bool(False)
process.siPixelDigis.CablingMapLabel =  cms.string("")
process.siPixelDigis.UseQualityInfo = cms.bool(True)

#Pilot Blade Digis
process.PBDigis = process.siPixelDigis.clone()
process.PBDigis.UsePilotBlade = cms.bool(True)
process.PBDigis.CablingMapLabel =  cms.string("pilotBlade")
process.PBDigis.UseQualityInfo = cms.bool(False)
	
#Pilot Blade Clusters
from CondTools.SiPixel.SiPixelGainCalibrationService_cfi import *
process.PBClusters = cms.EDProducer("SiPixelClusterProducer",
	SiPixelGainCalibrationServiceParameters,
	src = cms.InputTag("PBDigis"),
	ChannelThreshold = cms.int32(1000),
	MissCalibrate = cms.untracked.bool(True),
	SplitClusters = cms.bool(False),
	VCaltoElectronGain = cms.int32(65),
	VCaltoElectronOffset = cms.int32(-414),                          
	payloadType = cms.string('Offline'),
	SeedThreshold = cms.int32(1000),
	ClusterThreshold = cms.double(4000.0),
	maxNumberOfClusters = cms.int32(-1),
)

#Pilot Blade RecHits
process.PBRecHits = cms.EDProducer("SiPixelRecHitConverter",
        src = cms.InputTag("PBClusters"),
        CPE = cms.string('PixelCPEGeneric'),
        VerboseLevel = cms.untracked.int32(0),
)
#--------------------- EndPath -------------------------
process.PBDigi_step = cms.Path(process.PBDigis)
process.pilotBladeReco_step = cms.Path(
        process.PBClusters*
        process.PBRecHits
)
#-------------------------------------------------------

# New Schedule definitions
#	process.PBDigi_step,
#	process.pilotBladeReco_step,
'''
