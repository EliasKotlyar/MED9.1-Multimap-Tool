# How to Adapt to another MED91 Binary:


### Checking Compatibility.

Run med9info tool on your binary. Check the Bosch Software Version.

If you have "A4.8.6" or above , this tool should work

If you have a version below "A4.8.6" (for example: "A4.7.6") - it will probably not work.

Reason is, that the vkKraQu variable was introduced somewhere between 4.7.6 and 4.8.6 


### Finding Variable Locations

To make this tool work, you need to find 4 different locations in your file.

I will name them accordingly to the yaml:

"Payload Address" = insert_payload->address

"B_fgr" =   insert_payload->variables->B_fgr

"vkKraQu" =   insert_payload->variables->vkKraQu

"20ms_loop" = insert_jmp->address


#### Finding Payload Address:

Should be pretty easy, this is basically a free space spot where the payload will be patched.

Look out for big chunks of 0x00 or 0xFF with your hex editor. Insert address there. 

Most of the time 0x07e130 should work. 

### Finding B_fgr & vkKraQu

This 2 are more complicated. You will have to use either a matching A2L file to find them, or compare

your binary with Ghidra/IDA Pro to a well documented one (1Q0907115C_0040). Usually vkKraQu is pretty easy to spot

because you can just search for LDRXN table pointer, and look at the xrefs. B_fgr can be found by using signatures. 


### 20ms_loop

This is basically the address of a void function call in a loop function which is triggered every 20ms

Find "r20msCtr"(with A2L). Check where its being used, and check for a void function call(which returns immidiately) 








