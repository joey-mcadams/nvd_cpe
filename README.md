# NVD NPE Practical

This is the various code needed to satisfy the NVD CPE practical.

In the root of this folder, I need the following two files. 

    official-cpe-dictionary_v2.2.xml
    official-cpe-dictionary_v2.3.xml

These are available at 

https://nvd.nist.gov/products/cpe

To run all the code

```shell {interactive=True}
python3 main.py
```

Unit tests are available throughout the project. For the API tests, I would have rather used a Faker/Factory pattern, 
but I'm not sure if that would run afoul of the project requirements. So I did the test data the hard way. 

## Part2 discussion 

Still having memory issues. I think I'm around 20Mb total memory. This is difficult due to a limitation in OSX. 
RLIMIT isn't an available resource to edit in the underlying C libs on OSX. 

### check_cpe

This should be an `On` operation. It simply marches through the file and breaks if it finds the correct CPE. Worst case will be On

### get_top_10_products

This should be an `O2n+10` operation. The first `n` will be marching through the data and populating the hash with product-vendor counts. 
the second `n` will be sorting the data. Finally, `+10` for cutting off the front 10 and converting them to tuples. 

## NOTES

CPE Paser partially taken from: 
https://github.com/sabuhish/cpe-parser

It got pretty heavily edited in the end, but I really liked the dict(zip()) to put the CPE objects together. I moved
that out and into code that interacts with the model. 