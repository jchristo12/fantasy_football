SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `block`
-- Table structure for table `block`
--

CREATE TABLE `BLOCK` (
  `pid` int(7) NOT NULL,
  `blk` varchar(7) NOT NULL,
  `brcv` varchar(7) DEFAULT NULL,
  `type` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Blocked Punts, Field Goal Attempts, etc.';

-- --------------------------------------------------------

--
-- Table structure for table `conv`
--

CREATE TABLE `CONV` (
  `pid` int(7) NOT NULL,
  `type` varchar(4) NOT NULL,
  `bc` varchar(7) DEFAULT NULL,
  `psr` varchar(7) DEFAULT NULL,
  `trg` varchar(7) DEFAULT NULL,
  `conv` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='2 Point Conversion Attempts (Y=Success, N=Fail)';

-- --------------------------------------------------------

--
-- Table structure for table `defense`
--

CREATE TABLE `DEFENSE` (
  `uid` int(6) NOT NULL,
  `gid` int(5) NOT NULL,
  `player` varchar(7) NOT NULL,
  `solo` decimal(3,1) NOT NULL,
  `comb` decimal(3,1) NOT NULL,
  `sck` decimal(2,1) NOT NULL,
  `saf` tinyint(1) NOT NULL,
  `blk` tinyint(1) NOT NULL,
  `ints` tinyint(1) NOT NULL,
  `pdef` tinyint(1) NOT NULL,
  `frcv` tinyint(1) NOT NULL,
  `forc` tinyint(1) NOT NULL,
  `tdd` tinyint(1) NOT NULL,
  `rety` int(3) NOT NULL,
  `tdret` tinyint(1) NOT NULL,
  `peny` tinyint(2) NOT NULL,
  `snp` tinyint(2) NOT NULL,
  `fp` decimal(4,2) NOT NULL,
  `fp2` decimal(4,2) NOT NULL,
  `game` tinyint(2) NOT NULL,
  `seas` tinyint(2) NOT NULL,
  `year` int(4) NOT NULL,
  `team` varchar(3) NOT NULL,
  `posd` varchar(8) NOT NULL,
  `jnum` tinyint(2) NOT NULL,
  `dcp` tinyint(1) NOT NULL,
  `nflid` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `drive`
--

CREATE TABLE `DRIVE` (
  `uid` int(6) NOT NULL,
  `gid` int(7) NOT NULL,
  `fpid` int(7) NOT NULL,
  `tname` varchar(3) NOT NULL,
  `drvn` tinyint(2) NOT NULL,
  `obt` varchar(4) DEFAULT NULL,
  `qtr` tinyint(1) NOT NULL,
  `min` tinyint(2) NOT NULL,
  `sec` tinyint(2) NOT NULL,
  `yfog` tinyint(2) NOT NULL,
  `plays` tinyint(2) NOT NULL,
  `succ` tinyint(2) NOT NULL,
  `rfd` tinyint(2) NOT NULL,
  `pfd` tinyint(2) NOT NULL,
  `ofd` tinyint(2) NOT NULL,
  `ry` int(3) NOT NULL,
  `ra` tinyint(2) NOT NULL,
  `py` int(3) NOT NULL,
  `pa` tinyint(2) NOT NULL,
  `pc` tinyint(2) NOT NULL,
  `peyf` tinyint(2) NOT NULL,
  `peya` tinyint(2) NOT NULL,
  `net` int(3) NOT NULL,
  `res` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `fgxp`
--

CREATE TABLE `FGXP` (
  `pid` int(7) NOT NULL,
  `fgxp` varchar(2) NOT NULL,
  `fkicker` varchar(7) NOT NULL,
  `dist` tinyint(2) NOT NULL,
  `good` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `fumble`
--

CREATE TABLE `FUMBLE` (
  `pid` int(7) NOT NULL,
  `fum` varchar(7) NOT NULL,
  `frcv` varchar(7) DEFAULT NULL,
  `fry` int(3) NOT NULL,
  `forc` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE `GAME` (
  `gid` int(5) NOT NULL,
  `seas` int(4) NOT NULL,
  `wk` tinyint(2) NOT NULL,
  `day` varchar(3) NOT NULL,
  `v` varchar(3) NOT NULL,
  `h` varchar(3) NOT NULL,
  `stad` varchar(45) NOT NULL,
  `temp` varchar(4) DEFAULT NULL,
  `humd` varchar(4) DEFAULT NULL,
  `wspd` varchar(4) DEFAULT NULL,
  `wdir` varchar(4) DEFAULT NULL,
  `cond` varchar(15) DEFAULT NULL,
  `surf` varchar(30) NOT NULL,
  `ou` decimal(3,1) NOT NULL,
  `sprv` decimal(3,1) NOT NULL,
  `ptsv` tinyint(2) NOT NULL,
  `ptsh` tinyint(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `injury`
--

CREATE TABLE `INJURY` (
  `uid` int(6) NOT NULL,
  `gid` int(7) NOT NULL,
  `player` varchar(7) NOT NULL,
  `team` varchar(3) NOT NULL,
  `details` varchar(25) DEFAULT NULL,
  `pstat` varchar(35) DEFAULT NULL,
  `gstat` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Player injury status from official league reports';

-- --------------------------------------------------------

--
-- Table structure for table `intercpt`
--

CREATE TABLE `INTERCEPT` (
  `pid` int(7) NOT NULL,
  `psr` varchar(7) NOT NULL,
  `ints` varchar(7) NOT NULL,
  `iry` tinyint(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Interceptions';

-- --------------------------------------------------------

--
-- Table structure for table `kicker`
--

CREATE TABLE `KICKER` (
  `uid` int(6) NOT NULL,
  `gid` int(5) NOT NULL,
  `player` varchar(7) NOT NULL,
  `pat` tinyint(1) NOT NULL,
  `fgs` tinyint(1) NOT NULL,
  `fgm` tinyint(1) NOT NULL,
  `fgl` tinyint(1) NOT NULL,
  `fp` decimal(3,1) NOT NULL,
  `game` tinyint(2) NOT NULL,
  `seas` tinyint(2) NOT NULL,
  `year` int(4) NOT NULL,
  `team` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='FGS: 0 - 39 yds; FGM: 40 - 49 yds; FGL: 50+ yds';

-- --------------------------------------------------------

--
-- Table structure for table `koff`
--

CREATE TABLE `KOFF` (
  `pid` int(7) NOT NULL,
  `kicker` varchar(7) NOT NULL,
  `kgro` tinyint(2) NOT NULL,
  `knet` tinyint(2) NOT NULL,
  `ktb` tinyint(1) NOT NULL,
  `kr` varchar(7) DEFAULT NULL,
  `kry` tinyint(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `offense`
--

CREATE TABLE `OFFENSE` (
  `uid` int(6) NOT NULL,
  `gid` int(5) NOT NULL,
  `player` varchar(7) NOT NULL,
  `pa` tinyint(2) NOT NULL,
  `pc` tinyint(2) NOT NULL,
  `py` int(3) NOT NULL,
  `ints` tinyint(1) NOT NULL,
  `tdp` tinyint(1) NOT NULL,
  `ra` tinyint(2) NOT NULL,
  `sra` tinyint(2) NOT NULL,
  `ry` int(3) NOT NULL,
  `tdr` tinyint(1) NOT NULL,
  `trg` tinyint(2) NOT NULL,
  `rec` tinyint(2) NOT NULL,
  `recy` int(3) NOT NULL,
  `tdrec` tinyint(1) NOT NULL,
  `ret` tinyint(2) NOT NULL,
  `rety` int(3) NOT NULL,
  `tdret` tinyint(1) NOT NULL,
  `fuml` tinyint(1) NOT NULL,
  `peny` tinyint(2) NOT NULL,
  `conv` tinyint(1) NOT NULL,
  `snp` tinyint(2) NOT NULL,
  `fp` decimal(4,2) NOT NULL,
  `fp2` decimal(4,2) NOT NULL,
  `fp3` decimal(4,2) NOT NULL,
  `game` tinyint(2) NOT NULL,
  `seas` tinyint(2) NOT NULL,
  `year` int(4) NOT NULL,
  `team` varchar(3) NOT NULL,
  `posd` varchar(8) NOT NULL,
  `jnum` tinyint(2) NOT NULL,
  `dcp` tinyint(1) NOT NULL,
  `nflid` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `pass`
--

CREATE TABLE `PASS` (
  `pid` int(7) NOT NULL,
  `psr` varchar(7) NOT NULL,
  `trg` varchar(7) DEFAULT NULL,
  `loc` varchar(2) NOT NULL,
  `yds` tinyint(3) NOT NULL,
  `comp` tinyint(1) NOT NULL,
  `succ` tinyint(1) NOT NULL,
  `spk` tinyint(1) NOT NULL,
  `dfb` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Table structure for table `penalty`
--

CREATE TABLE `PENALTY` (
  `uid` int(6) NOT NULL,
  `pid` int(7) NOT NULL,
  `ptm` varchar(3) NOT NULL,
  `pen` varchar(7) DEFAULT NULL,
  `desc` varchar(40) NOT NULL,
  `cat` tinyint(1) NOT NULL,
  `pey` tinyint(2) NOT NULL,
  `act` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `play`
--

CREATE TABLE `PLAY` (
  `gid` int(5) NOT NULL,
  `pid` int(7) NOT NULL,
  `off` varchar(3) NOT NULL,
  `def` varchar(3) NOT NULL,
  `type` varchar(4) NOT NULL,
  `dseq` tinyint(2) NOT NULL,
  `len` tinyint(2) NOT NULL,
  `qtr` tinyint(1) NOT NULL,
  `min` tinyint(2) NOT NULL,
  `sec` tinyint(2) NOT NULL,
  `ptso` tinyint(2) NOT NULL,
  `ptsd` tinyint(2) NOT NULL,
  `timo` tinyint(2) NOT NULL,
  `timd` tinyint(2) NOT NULL,
  `dwn` tinyint(1) NOT NULL,
  `ytg` tinyint(2) NOT NULL,
  `yfog` tinyint(2) NOT NULL,
  `zone` tinyint(1) NOT NULL,
  `fd` tinyint(1) NOT NULL,
  `sg` tinyint(1) NOT NULL,
  `nh` tinyint(1) NOT NULL,
  `pts` tinyint(1) NOT NULL,
  `tck` tinyint(1) NOT NULL,
  `sk` tinyint(1) NOT NULL,
  `pen` tinyint(1) NOT NULL,
  `ints` tinyint(1) NOT NULL,
  `fum` tinyint(1) NOT NULL,
  `saf` tinyint(1) NOT NULL,
  `blk` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `PLAYER` (
  `player` varchar(7) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `pname` varchar(25) NOT NULL,
  `pos1` varchar(2) NOT NULL,
  `pos2` varchar(2) DEFAULT NULL,
  `height` tinyint(2) NOT NULL,
  `weight` int(3) NOT NULL,
  `dob` varchar(10) DEFAULT NULL,
  `forty` decimal(3,2) NOT NULL,
  `bench` tinyint(2) NOT NULL,
  `vertical` decimal(3,1) NOT NULL,
  `broad` int(3) NOT NULL,
  `shuttle` decimal(3,2) NOT NULL,
  `cone` decimal(3,2) NOT NULL,
  `arm` decimal(5,3) NOT NULL,
  `hand` decimal(5,3) NOT NULL,
  `dpos` int(3) NOT NULL,
  `col` varchar(35) NOT NULL,
  `dv` varchar(35) DEFAULT NULL,
  `start` int(4) NOT NULL,
  `cteam` varchar(3) NOT NULL,
  `posd` varchar(8) NOT NULL,
  `jnum` tinyint(2) NOT NULL,
  `dcp` tinyint(1) NOT NULL,
  `nflid` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `punt`
--

CREATE TABLE `PUNT` (
  `pid` int(7) NOT NULL,
  `punter` varchar(7) NOT NULL,
  `pgro` tinyint(2) NOT NULL,
  `pnet` tinyint(2) NOT NULL,
  `ptb` tinyint(1) NOT NULL,
  `pr` varchar(7) DEFAULT NULL,
  `pry` tinyint(3) NOT NULL,
  `pfc` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `redzone`
--

CREATE TABLE `REDZONE` (
  `uid` int(6) NOT NULL,
  `gid` int(5) NOT NULL,
  `player` varchar(7) NOT NULL,
  `pa` tinyint(2) NOT NULL,
  `pc` tinyint(2) NOT NULL,
  `py` int(3) NOT NULL,
  `ints` tinyint(1) NOT NULL,
  `ra` tinyint(2) NOT NULL,
  `sra` tinyint(2) NOT NULL,
  `ry` int(3) NOT NULL,
  `trg` tinyint(2) NOT NULL,
  `rec` tinyint(2) NOT NULL,
  `recy` int(3) NOT NULL,
  `fuml` tinyint(1) NOT NULL,
  `peny` tinyint(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `rush`
--

CREATE TABLE `RUSH` (
  `pid` int(7) NOT NULL,
  `bc` varchar(7) NOT NULL,
  `dir` varchar(2) NOT NULL,
  `yds` tinyint(3) NOT NULL,
  `succ` tinyint(1) NOT NULL,
  `kne` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sack`
--

CREATE TABLE `SACK` (
  `uid` int(6) NOT NULL,
  `pid` int(7) NOT NULL,
  `qb` varchar(7) NOT NULL,
  `sk` varchar(7) NOT NULL,
  `value` decimal(2,1) NOT NULL,
  `ydsl` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `safety`
--

CREATE TABLE `SAFETY` (
  `pid` int(7) NOT NULL,
  `saf` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

CREATE TABLE `SCHEDULE` (
  `gid` int(5) NOT NULL,
  `seas` int(4) NOT NULL,
  `wk` tinyint(2) NOT NULL,
  `day` varchar(3) NOT NULL,
  `date` text NOT NULL,
  `v` varchar(3) NOT NULL,
  `h` varchar(3) NOT NULL,
  `stad` varchar(45) NOT NULL,
  `surf` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `snap`
--

CREATE TABLE `SNAP` (
  `uid` int(6) NOT NULL,
  `gid` int(5) NOT NULL,
  `tname` varchar(3) NOT NULL,
  `player` varchar(7) NOT NULL,
  `posd` varchar(8) NOT NULL,
  `poss` varchar(8) DEFAULT NULL,
  `snp` tinyint(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Play snaps for offense and defense';

-- --------------------------------------------------------

--
-- Table structure for table `tackle`
--

CREATE TABLE `TACKLE` (
  `uid` int(7) NOT NULL,
  `pid` int(7) NOT NULL,
  `tck` varchar(7) NOT NULL,
  `value` decimal(2,1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Special teams tackles are not counted (ie, kickoffs, punts)';

-- --------------------------------------------------------

--
-- Table structure for table `td`
--

CREATE TABLE `TD` (
  `pid` int(7) NOT NULL,
  `qtr` tinyint(1) NOT NULL,
  `min` tinyint(2) NOT NULL,
  `sec` tinyint(2) NOT NULL,
  `dwn` tinyint(1) NOT NULL,
  `yds` tinyint(3) NOT NULL,
  `pts` tinyint(2) NOT NULL,
  `player` varchar(7) DEFAULT NULL,
  `type` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `TEAM` (
  `tid` int(5) NOT NULL,
  `gid` int(5) NOT NULL,
  `tname` varchar(3) NOT NULL,
  `pts` tinyint(2) NOT NULL,
  `q1p` tinyint(2) NOT NULL,
  `q2p` tinyint(2) NOT NULL,
  `q3p` tinyint(2) NOT NULL,
  `q4p` tinyint(2) NOT NULL,
  `rfd` tinyint(2) NOT NULL,
  `pfd` tinyint(2) NOT NULL,
  `ifd` tinyint(2) NOT NULL,
  `ry` int(3) NOT NULL,
  `ra` tinyint(2) NOT NULL,
  `py` int(3) NOT NULL,
  `pa` tinyint(2) NOT NULL,
  `pc` tinyint(2) NOT NULL,
  `sk` tinyint(2) NOT NULL,
  `ints` tinyint(1) NOT NULL,
  `fum` tinyint(1) NOT NULL,
  `pu` tinyint(2) NOT NULL,
  `gpy` int(3) NOT NULL,
  `pr` tinyint(2) NOT NULL,
  `pry` int(3) NOT NULL,
  `kr` tinyint(2) NOT NULL,
  `kry` int(3) NOT NULL,
  `ir` tinyint(1) NOT NULL,
  `iry` int(3) NOT NULL,
  `pen` int(3) NOT NULL,
  `top` decimal(3,1) NOT NULL,
  `td` tinyint(1) NOT NULL,
  `tdr` tinyint(1) NOT NULL,
  `tdp` tinyint(1) NOT NULL,
  `tdt` tinyint(1) NOT NULL,
  `fgm` tinyint(1) NOT NULL,
  `fgat` tinyint(2) NOT NULL,
  `fgy` int(3) NOT NULL,
  `rza` tinyint(2) NOT NULL,
  `rzc` tinyint(1) NOT NULL,
  `bry` int(3) NOT NULL,
  `bpy` int(3) NOT NULL,
  `srp` tinyint(2) NOT NULL,
  `s1rp` tinyint(2) NOT NULL,
  `s2rp` tinyint(2) NOT NULL,
  `s3rp` tinyint(2) NOT NULL,
  `spp` tinyint(2) NOT NULL,
  `s1pp` tinyint(2) NOT NULL,
  `s2pp` tinyint(2) NOT NULL,
  `s3pp` tinyint(2) NOT NULL,
  `lea` tinyint(2) NOT NULL,
  `ley` int(3) NOT NULL,
  `lta` tinyint(2) NOT NULL,
  `lty` int(3) NOT NULL,
  `lga` tinyint(2) NOT NULL,
  `lgy` int(3) NOT NULL,
  `mda` tinyint(2) NOT NULL,
  `mdy` int(3) NOT NULL,
  `rga` tinyint(2) NOT NULL,
  `rgy` int(3) NOT NULL,
  `rta` tinyint(2) NOT NULL,
  `rty` int(3) NOT NULL,
  `rea` tinyint(2) NOT NULL,
  `rey` int(3) NOT NULL,
  `r1a` tinyint(2) NOT NULL,
  `r1y` int(3) NOT NULL,
  `r2a` tinyint(2) NOT NULL,
  `r2y` int(3) NOT NULL,
  `r3a` tinyint(2) NOT NULL,
  `r3y` int(3) NOT NULL,
  `qba` tinyint(2) NOT NULL,
  `qby` int(3) NOT NULL,
  `sla` tinyint(2) NOT NULL,
  `sly` int(3) NOT NULL,
  `sma` tinyint(2) NOT NULL,
  `smy` int(3) NOT NULL,
  `sra` tinyint(2) NOT NULL,
  `sry` int(3) NOT NULL,
  `dla` tinyint(2) NOT NULL,
  `dly` int(3) NOT NULL,
  `dma` tinyint(2) NOT NULL,
  `dmy` int(3) NOT NULL,
  `dra` tinyint(2) NOT NULL,
  `dry` int(3) NOT NULL,
  `wr1a` tinyint(2) NOT NULL,
  `wr1y` int(3) NOT NULL,
  `wr3a` tinyint(2) NOT NULL,
  `wr3y` int(3) NOT NULL,
  `tea` tinyint(2) NOT NULL,
  `tey` int(3) NOT NULL,
  `rba` tinyint(2) NOT NULL,
  `rby` int(3) NOT NULL,
  `sga` tinyint(2) NOT NULL,
  `sgy` int(3) NOT NULL,
  `p1a` tinyint(2) NOT NULL,
  `p1y` int(3) NOT NULL,
  `p2a` tinyint(2) NOT NULL,
  `p2y` int(3) NOT NULL,
  `p3a` tinyint(2) NOT NULL,
  `p3y` int(3) NOT NULL,
  `spc` tinyint(2) NOT NULL,
  `mpc` tinyint(2) NOT NULL,
  `lpc` tinyint(2) NOT NULL,
  `q1ra` tinyint(2) NOT NULL,
  `q1ry` int(3) NOT NULL,
  `q1pa` tinyint(2) NOT NULL,
  `q1py` int(3) NOT NULL,
  `lcra` tinyint(2) NOT NULL,
  `lcry` int(3) NOT NULL,
  `lcpa` tinyint(2) NOT NULL,
  `lcpy` int(3) NOT NULL,
  `rzra` tinyint(2) NOT NULL,
  `rzry` int(3) NOT NULL,
  `rzpa` tinyint(2) NOT NULL,
  `rzpy` int(3) NOT NULL,
  `sky` int(3) NOT NULL,
  `lbs` decimal(3,1) NOT NULL,
  `dbs` decimal(3,1) NOT NULL,
  `sfpy` int(3) NOT NULL,
  `drv` tinyint(2) NOT NULL,
  `npy` int(3) NOT NULL,
  `tb` tinyint(1) NOT NULL,
  `i20` tinyint(1) NOT NULL,
  `rtd` tinyint(1) NOT NULL,
  `lnr` decimal(3,1) NOT NULL,
  `lnp` decimal(3,1) NOT NULL,
  `lbr` decimal(3,1) NOT NULL,
  `lbp` decimal(3,1) NOT NULL,
  `dbr` decimal(3,1) NOT NULL,
  `dbp` decimal(3,1) NOT NULL,
  `nha` tinyint(2) NOT NULL,
  `s3a` tinyint(2) NOT NULL,
  `s3c` tinyint(2) NOT NULL,
  `l3a` tinyint(2) NOT NULL,
  `l3c` tinyint(2) NOT NULL,
  `stf` tinyint(2) NOT NULL,
  `dp` tinyint(2) NOT NULL,
  `fsp` tinyint(2) NOT NULL,
  `ohp` tinyint(2) NOT NULL,
  `pbep` tinyint(1) NOT NULL,
  `dlp` tinyint(1) NOT NULL,
  `dsp` tinyint(1) NOT NULL,
  `dum` tinyint(1) NOT NULL,
  `pfn` tinyint(1) NOT NULL,
  `snpo` tinyint(2) NOT NULL,
  `snpd` tinyint(2) NOT NULL,
  `saf` tinyint(1) NOT NULL,
  `blk` tinyint(1) NOT NULL,
  `fp` tinyint(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `pbp`
--

CREATE TABLE `PBP` (
  `gid` int(5) NOT NULL,
  `pid` int(7) NOT NULL,
  `detail` text NOT NULL,
  `off` varchar(3) NOT NULL,
  `def` varchar(3) NOT NULL,
  `type` varchar(4) NOT NULL,
  `dseq` tinyint(2) NOT NULL,
  `len` tinyint(2) NOT NULL,
  `qtr` tinyint(1) NOT NULL,
  `min` tinyint(2) NOT NULL,
  `sec` tinyint(2) NOT NULL,
  `ptso` tinyint(2) NOT NULL,
  `ptsd` tinyint(2) NOT NULL,
  `timo` tinyint(1) NOT NULL,
  `timd` tinyint(1) NOT NULL,
  `dwn` varchar(1) DEFAULT NULL,
  `ytg` varchar(2) DEFAULT NULL,
  `yfog` varchar(2) DEFAULT NULL,
  `zone` varchar(1) DEFAULT NULL,
  `yds` varchar(3) DEFAULT NULL,
  `succ` varchar(1) DEFAULT NULL,
  `fd` varchar(1) DEFAULT NULL,
  `sg` varchar(1) DEFAULT NULL,
  `nh` varchar(1) DEFAULT NULL,
  `pts` varchar(2) DEFAULT NULL,
  `bc` varchar(7) DEFAULT NULL,
  `kne` varchar(1) DEFAULT NULL,
  `dir` varchar(2) DEFAULT NULL,
  `rtck1` varchar(7) DEFAULT NULL,
  `rtck2` varchar(7) DEFAULT NULL,
  `psr` varchar(7) DEFAULT NULL,
  `comp` varchar(1) DEFAULT NULL,
  `spk` varchar(1) DEFAULT NULL,
  `loc` varchar(2) DEFAULT NULL,
  `trg` varchar(7) DEFAULT NULL,
  `dfb` varchar(7) DEFAULT NULL,
  `ptck1` varchar(7) DEFAULT NULL,
  `ptck2` varchar(7) DEFAULT NULL,
  `sk1` varchar(7) DEFAULT NULL,
  `sk2` varchar(7) DEFAULT NULL,
  `ptm1` varchar(3) DEFAULT NULL,
  `pen1` varchar(7) DEFAULT NULL,
  `desc1` varchar(40) DEFAULT NULL,
  `cat1` varchar(1) DEFAULT NULL,
  `pey1` varchar(2) DEFAULT NULL,
  `act1` varchar(1) DEFAULT NULL,
  `ptm2` varchar(3) DEFAULT NULL,
  `pen2` varchar(7) DEFAULT NULL,
  `desc2` varchar(40) DEFAULT NULL,
  `cat2` varchar(1) DEFAULT NULL,
  `pey2` varchar(2) DEFAULT NULL,
  `act2` varchar(1) DEFAULT NULL,
  `ptm3` varchar(3) DEFAULT NULL,
  `pen3` varchar(7) DEFAULT NULL,
  `desc3` varchar(40) DEFAULT NULL,
  `cat3` varchar(1) DEFAULT NULL,
  `pey3` varchar(2) DEFAULT NULL,
  `act3` varchar(1) DEFAULT NULL,
  `ints` varchar(7) DEFAULT NULL,
  `iry` varchar(3) DEFAULT NULL,
  `fum` varchar(7) DEFAULT NULL,
  `frcv` varchar(7) DEFAULT NULL,
  `fry` varchar(3) DEFAULT NULL,
  `forc` varchar(7) DEFAULT NULL,
  `saf` varchar(7) DEFAULT NULL,
  `blk` varchar(7) DEFAULT NULL,
  `brcv` varchar(7) DEFAULT NULL,
  `fgxp` varchar(2) DEFAULT NULL,
  `fkicker` varchar(7) DEFAULT NULL,
  `dist` varchar(2) DEFAULT NULL,
  `good` varchar(1) DEFAULT NULL,
  `punter` varchar(7) DEFAULT NULL,
  `pgro` varchar(3) DEFAULT NULL,
  `pnet` varchar(3) DEFAULT NULL,
  `ptb` varchar(1) DEFAULT NULL,
  `pr` varchar(7) DEFAULT NULL,
  `pry` varchar(3) DEFAULT NULL,
  `pfc` varchar(1) DEFAULT NULL,
  `kicker` varchar(7) DEFAULT NULL,
  `kgro` varchar(3) DEFAULT NULL,
  `knet` varchar(3) DEFAULT NULL,
  `ktb` varchar(1) DEFAULT NULL,
  `kr` varchar(7) DEFAULT NULL,
  `kry` varchar(3) DEFAULT NULL 
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
--
-- Indexes for dumped tables
--

--
-- Indexes for table `block`
--
ALTER TABLE `BLOCK`
  ADD UNIQUE KEY `pid` (`pid`);

--
-- Indexes for table `conv`
--
ALTER TABLE `CONV`
  ADD UNIQUE KEY `pid` (`pid`);

--
-- Indexes for table `defense`
--
ALTER TABLE `DEFENSE`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `player` (`player`);

--
-- Indexes for table `drive`
--
ALTER TABLE `DRIVE`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `fpid` (`fpid`),
  ADD KEY `tname` (`tname`);

--
-- Indexes for table `fgxp`
--
ALTER TABLE `FGXP`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `fgxp` (`fgxp`);

--
-- Indexes for table `fumble`
--
ALTER TABLE `FUMBLE`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `fum` (`fum`);

--
-- Indexes for table `game`
--
ALTER TABLE `GAME`
  ADD UNIQUE KEY `gid` (`gid`),
  ADD KEY `seas` (`seas`);

--
-- Indexes for table `kicker`
--
ALTER TABLE `INJURY`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `player` (`player`);  

--
-- Indexes for table `intercpt`
--
ALTER TABLE `INTERCEPT`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `psr` (`psr`),
  ADD KEY `ints` (`ints`);

--
-- Indexes for table `kicker`
--
ALTER TABLE `KICKER`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `player` (`player`);

--
-- Indexes for table `koff`
--
ALTER TABLE `KOFF`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `kicker` (`kicker`);

--
-- Indexes for table `offense`
--
ALTER TABLE `OFFENSE`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `player` (`player`);

--
-- Indexes for table `pass`
--
ALTER TABLE `PASS`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `psr` (`psr`),
  ADD KEY `trg` (`trg`);

--
-- Indexes for table `penalty`
--
ALTER TABLE `PENALTY`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `play`
--
ALTER TABLE `PLAY`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `gid` (`gid`);

--
-- Indexes for table `player`
--
ALTER TABLE `PLAYER`
  ADD UNIQUE KEY `player` (`player`),
  ADD KEY `fname` (`fname`),
  ADD KEY `lname` (`lname`);

--
-- Indexes for table `punt`
--
ALTER TABLE `PUNT`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `punter` (`punter`);

--
-- Indexes for table `redzone`
--
ALTER TABLE `REDZONE`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `player` (`player`);

--
-- Indexes for table `rush`
--
ALTER TABLE `RUSH`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `bc` (`bc`);

--
-- Indexes for table `sack`
--
ALTER TABLE `SACK`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `pid` (`pid`),
  ADD KEY `qb` (`qb`),
  ADD KEY `sk` (`sk`);

--
-- Indexes for table `safety`
--
ALTER TABLE `SAFETY`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `saf` (`saf`);

--
-- Indexes for table `schedule`
--
ALTER TABLE `SCHEDULE`
  ADD UNIQUE KEY `gid` (`gid`);

--
-- Indexes for table `tackle`
--
ALTER TABLE `TACKLE`
  ADD UNIQUE KEY `uid` (`uid`),
  ADD KEY `pid` (`pid`),
  ADD KEY `tck` (`tck`);

--
-- Indexes for table `td`
--
ALTER TABLE `TD`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `player` (`player`);

--
-- Indexes for table `team`
--
ALTER TABLE `TEAM`
  ADD UNIQUE KEY `tid` (`tid`),
  ADD KEY `gid` (`gid`),
  ADD KEY `tname` (`tname`);
  
--
-- Indexes for table `pbp`
--
ALTER TABLE `PBP`
  ADD UNIQUE KEY `pid` (`pid`),
  ADD KEY `gid` (`gid`),
  ADD FULLTEXT KEY `detail` (`detail`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;