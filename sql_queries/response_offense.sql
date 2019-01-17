select concat(GAME.seas, "&", GAME.wk, "&", PLAYER.player) as pk,
	GAME.seas, GAME.wk, PLAYER.player, PLAYER.pos1, OFFENSE.py, OFFENSE.ints, OFFENSE.tdp,
	OFFENSE.ry, OFFENSE.tdr, OFFENSE.recy, OFFENSE.tdrec, OFFENSE.rety, OFFENSE.tdret,
    OFFENSE.fuml, OFFENSE.conv
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
-- limit 10
;