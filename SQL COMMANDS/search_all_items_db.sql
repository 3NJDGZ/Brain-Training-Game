select PlayerID, Username, replace(cast(aes_decrypt(Password, 'encryptionkey1234') as char(100)), Salt, ''), Salt
from Player;
-- select * 
-- from Player;
select * 
from CPS;
select * 
from Performance;
select * 
from Weights;
select * 
from CognitiveArea;
