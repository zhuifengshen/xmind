## Xmind2TestLink Guide

Now xmind2testlink has been upgraded to v2, it supports 2 kinds of conversion.

### v1 Rules

For old users (xmind2testlink v1), your xmind looks like below structure.

![xmind2testlink_v1](xmind2testlink_v1.png)

The output:

![xmind2testlink_v1_out](xmind2testlink_v1_out.png)

**Generally to say:**

1. The first sub topic => suite
2. The sub topic of suite => test case title
3. The sub topic of test case => test step
4. The sub topic of test step => expected result

### v2 Rules

Your input xmind looks like this:

![xmind2testlink_v2](xmind2testlink_v2.png)

The output:

![xmind2testlink_v2_out](xmind2testlink_v2_out.png)

**More about v2:**

1. Mark root topic with a **star marker**, this means **v2 xmind** file. (no matter what color of star maker)
2. First sub topic => it is still converted to suite
3. Test case title will be combined by sub topics, until:
   1. Child topic is marked with priority
   2. Current topic is end topic

By default, the title parts are connected by **blank space**, you can define the `connector` by last char of root topic, like this.

![xmind2testlink_v2_sep](xmind2testlink_v2_sep.png)

Then the output will be changed to:

![xmind2testlink_v2_sep_out](xmind2testlink_v2_sep_out.png)

Note: only valid chars can be used as a `connector`. 

### More detail

1. `Notes` for a test suite => `details` in TestLink.
2. `Notes` for a test case => `summary` in TestLink.
3. `Comments` for a test case => `preconditions` in TestLink.
4. `Priority` maker for a test case => `importance` in TestLink.
5. Sub topics for a test case will be treated as test steps.
   - It is okay to design test step **with action** but **without expected results**.
6. Use `!` to ignore any topic that you don't want to convert.
7. Root topic will not be converted, it is target suite node in TestLink.
8. Free topic and notes will not be converted.
9. Only the first sheet in xmind will be converted.

**Download the sample xmind files:**

- [test case by xmind v1.xmind](test_case_by_xmind_v1.xmind)
- [test case by xmind v2.xmind](test_case_by_xmind_v2.xmind)


## Reference

- https://github.com/tobyqin/xmind2testlink

