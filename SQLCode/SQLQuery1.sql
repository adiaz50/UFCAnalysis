--SELECT FIGHTER, [W/L], [ROUND], METHOD, OPPONENT
--From UFCData..UFCDB
--WHERE FIGHTER like '%Jon Jones%'
--Order by 2

-- Select Data that we will be using
Select FIGHTER, [W/L], [ROUND], [TIMESTOPPAGE], METHOD, [TOTAL.STR.THROWN], OPPONENT
From UFCData..TESTINGV3
order by 6 DESC