select GAME.seas, GAME.wk, PLAYER.pos1, OFFENSE.py, OFFENSE.ints, OFFENSE.tdp, OFFENSE.ry,
	OFFENSE.tdr, OFFENSE.recy, OFFENSE.tdrec, OFFENSE.rety, OFFENSE.tdret, OFFENSE.fuml,OFFENSE.conv,
    round(OFFENSE.py / 25 +
			OFFENSE.ints * -2 +
            OFFENSE.tdp * 4 +
            OFFENSE.ry / 10 +
            OFFENSE.tdr * 6 +
            OFFENSE.recy / 10 +
            OFFENSE.tdrec * 6 +
			OFFENSE.rety / 35 +
			OFFENSE.tdret * 6 +
			OFFENSE.fuml * -2 +
			OFFENSE.conv * 2, 2) as fpts_off
from OFFENSE
left join GAME
	on OFFENSE.gid = GAME.gid
left join PLAYER
	on OFFENSE.player = PLAYER.player
where GAME.wk <= 17
	and
	(PLAYER.pos1 = "QB" or
	PLAYER.pos1 = "RB" or 
	PLAYER.pos1 = "WR" or 
	PLAYER.pos1 = "TE" or 
	PLAYER.pos1 = "K"
	)
;