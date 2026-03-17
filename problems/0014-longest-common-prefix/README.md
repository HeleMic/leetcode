# 14. Longest Common Prefix

**Link:** <https://leetcode.com/problems/longest-common-prefix/>  
**Difficulty:** Easy  
**Topics:** Array, String, Trie

## Description

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

## Examples

**Example 1:**

```text
Input: strs = [&quot;flower&quot;,&quot;flow&quot;,&quot;flight&quot;]
Output: &quot;fl&quot;
```

**Example 2:**

```text
Input: strs = [&quot;dog&quot;,&quot;racecar&quot;,&quot;car&quot;]
Output: &quot;&quot;
Explanation: There is no common prefix among the input strings.
```

## Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i] consists of only lowercase English letters if it is non-empty.`
