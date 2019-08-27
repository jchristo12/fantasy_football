select concat(GAME.gid, "&", PLAYER.player) as pk,
	GAME.gid, GAME.seas, GAME.wk, PLAYER.player, PLAYER.pos1, OFFENSE.py, OFFENSE.ints, OFFENSE.tdp,
	OFFENSE.ry, OFFENSE.tdr, OFFENSE.recy, OFFENSE.tdrec, OFFENSE.rety, OFFENSE.tdret,
    OFFENSE.fuml, OFFENSE.conv
from OFFENSE
left join GAME
	on OFFENSE.gid = GAME.gid
left join PLAYER
	on OFFENSE.player = PLAYER.player
where GAME.wk <= 16
	and
	PLAYER.pos1 in ("QB", "RB", "WR", "TE", "K")
;