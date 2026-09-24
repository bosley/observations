
# The Scenario 

Consider the following: 

You have a table big enough for two boxes.
A coworker takes boxes from the pile and places two of them on the table
In the box there could be something, or it could be empty. We won't know until we open them and check.

Since we have two boxes we can say we have `box-left` and `box-right`. Before we open the boxes we know each could be empty, but it could also contain something (which counts if its multiple somethings).

This means `box-left` can be `something` or `empty`, and `box-right` could be `something` or `empty`. Lets make a chart:

| State | box-left | box-right |
|---|---|---|
| A | empty | empty |
| B | empty | something |
| C | something | empty |
| D | something | something |

At this job we will be told to play one of three roles. These roles dictate if we are to push an intimidatingly large red button. The three roles are that of `and` `or` and the exclusive `xor`. 

When you arrive at your station there will be a sign that states which role you are playing in neon pink.

In the role `and` you hit the button if and only if (iff) both boxes contain something.
Similarly to one might intuit by the name, `or` requires you to hit the button if the left box OR the right box has something in it.

The final `xor` means "exclusive" or. This states that you must hit the button iff one and ONLY one of the boxes contains something.

Lets make a full chart to see our roles and states that tell us if we hit the button. 
For simplicity of notation I will now represent "something" as "1" and "empty" as "0".
When we need to hit the button we use Y and when we should skip we use S.


| | A (0,0) | B (0,1) | C (1,0) | D (1,1) |
|---|---|---|---|---|
| `and` | SKIP | SKIP | SKIP | PRESS |
| `or` | SKIP | PRESS | PRESS | PRESS |
| `xor` | SKIP | PRESS | PRESS | SKIP |

Each row is a role. Each column is one of the four combinations from the first chart, A through D, where 0 means the box is empty and 1 means it holds something. The cell is what that role does with those two boxes. PRESS is hit the button, SKIP is don't.

For the sake of the example, if you dont press the button fast enough it counts as a skip. If an error occurs your coworkers will throw the boxes off the table and diaster will ensue. Make no mistakes.
For the sake of the example, if you dont press the button fast enough it counts as a skip. If an error occurs your coworkers will throw the boxes off the table and diaster will ensue. Make no mistakes.

# Gates

The sign on the wall is still how you know which job you showed up for. What the job makes you do is the row. For each of A, B, C, and D it says press or skip. A row fixed like that is called a gate. `and`, `or`, and `xor` are gates. The sign can also say `nand` or `nor`.

`nand` is the `and` row with PRESS and SKIP swapped. You skip only when both boxes have something. The other three states, you press.

`nor` is the `or` row with PRESS and SKIP swapped. You press only when both boxes are empty. The other three states, you skip.

Lets put them next to the rows they came from.

| | A (0,0) | B (0,1) | C (1,0) | D (1,1) |
|---|---|---|---|---|
| `and` | SKIP | SKIP | SKIP | PRESS |
| `nand` | PRESS | PRESS | PRESS | SKIP |
| `or` | SKIP | PRESS | PRESS | PRESS |
| `nor` | PRESS | SKIP | SKIP | SKIP |

`xor` still sits on the first chart. It presses when the boxes disagree. `nor` presses only when both are empty.

Say the sign says `nand` and you have already opened both. `box-left` has something, `box-right` is empty. Column C. The row says PRESS, so you hit the button. If `box-right` had something too, column D, you would skip. That is the only skip on the row.

Say the sign says `nor`. Both empty, column A, you press. `box-left` has something, `box-right` is empty, column C, you skip. A something in either box is enough to skip.

# Making shortcuts

Sometimes you don't need to open both boxes to know your answer. For the `and` gate, if you open `box-left` and it's empty, you already know to SKIP. It doesn't matter what's in `box-right`. You can set it aside without even opening it.

`or` works the opposite way. If `box-left` has something in it, you already know to PRESS. `box-right` is irrelevant.

`nand` and `nor` use the same early exits as `and` and `or`. What changed is the button. Empty `box-left` on `nand` means PRESS, and you can set `box-right` aside. Something in `box-left` on `nor` means SKIP, and the right box doesn't matter. If the left box doesn't settle it, you still open the right one.

`xor` is the one where you can never skip the second box. You have to open both. If `box-left` is empty you still don't know, and if `box-left` has something you still don't know. The answer depends on whether they match.

This is called short-circuit evaluation. The gate lets you stop early in some states, but not all of them.

# Estimating time

Every step in your shift costs time. Opening a box costs time. Looking inside and deciding if it's a 0 or a 1 costs time. Hitting the button costs time. Whatever happens after the button push costs time. And your coworker loading boxes onto your table in the first place costs time.

None of these steps are free, and they don't all cost the same. If we want the whole operation to run as fast as possible we have to start thinking about where that time goes. The shortcutting from the last section is one place. The rest of the optimizations grow from the same idea, every step you can skip or do cheaper is time you get back.

`xor` is the most expensive gate. It always costs you both boxes and a lengthy decision. In this problem space `and` is cheaper in most cases since three of the four states let you stop at the left box. `nand` exits early on the same boxes `and` does, and the button answer is swapped. But `or` can be the cheapest of all, iff `box-left` happens to be something, you know immediately and never touch the right box. `nor` gets that same exit off a something in `box-left`, and skips where `or` would press. Whether you're usually in that case depends on what your coworkers tend to load on your table (discuss: branch prediction).

# Cardinality

The term cardinality just means the number of something in some set (group). Without calling it out we did that above when we listed all the possible states. 

We have two boxes, each that we consider as "something" or "empty" which is two possible states that the boxes could be in. Since we can have `2` different things in each spot we can say that the problem set as a `cardinality` of `4` since 2 x 2 = 4.

The reason it matters is that the number of combinations can get out of hand really quickly. One box gives you 2 states. Two boxes gives you 4. Three boxes gives you 8. Each box you add doubles what you're dealing with. By the time you have a handful of boxes the chart is too big to think about informally and the cost estimates from the last section start to bite. Similarly, if the problem itself changed and suddenly we could have more than just "something" and "empty" regardless of the number of boxes, the chart would again become too unweildy to manage.

# Factorials and Combinatorics

When the problem stops being about flipping a box between two states and starts being about arranging things, the math changes a bit. Say instead of two states per box you have five boxes and you need to figure out every possible ordering of them. That's not multiplication anymore, that's a factorial.

5 boxes, all different, arranged in a line. The first spot has 5 choices, the second has 4, the third has 3, and so on. 5 x 4 x 3 x 2 x 1 = 120. Written as 5!. The number of arrangements of n things is n!.

Combinatorics is the broader field that contains this. Factorials are one tool in it. The question is how many ways you can pick from a set of things, or arrange them, under some set of rules. If order matters the answer is different than if it doesn't. If you can repeat choices the answer is different than if you can't.

Same reason cardinality mattered. Before you can estimate how long something takes to process, you need to know how many cases you're actually dealing with. Combinatorics is how you count that when the problem is arrangement or selection instead of just states.
