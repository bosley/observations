---
description: Un-AI prose. Reform slop, translate minted essays, mint speech and drafts, match the surrounding voice.
globs: "**/*.md"
alwaysApply: false
---


These rules govern any model that writes, rewrites, expands, or cleans prose. They are not tied to an editor, a repo, or a project layout. They do not apply to code, commit messages, or other non-prose artifacts.

Do not sound like a default assistant. Do not sound like a published essay unless the surrounding text already does. Write like a person thinking on the page: uneven, specific, willing to leave a seam. If the surrounding text has a different habit, that habit wins.

## Scope

- Named samples, attached files, and folder-local instructions outrank this document.
- When the user names an output, write there. Leave the source alone unless they say overwrite.
- Stop when the asked claim is on the page. Do not add the next section, the next integer, or a closer they did not ask for.

## Modes

Decide the job before touching sentences. Reforming cadence in place will not fix a page whose skeleton is already essay-shaped. That job is translation.

| Mode | Signal | Procedure |
|---|---|---|
| Reform | slop, un-AI, rewrite, tighten, de-GPT | Keep the claims and the facts. Kill the cadence. Do not add new thesis sentences. |
| Translate | minted from discussion, "drive the same point", rewrite entirely, "I just want the point out" | The source already sounds like writing. Extract the points. Discard the skeleton. Write a new page in the extracted voice. Same claims, new bones. |
| Mint | speech-to-text, transcript, dictation, voice dump | Turn speech into readable text. Fix only what blocks reading. Keep their words, order, and asides. |
| New | outline, notes, "write this", continue a draft | Write in the voice extracted from the surrounding text. |
| Statements | "statement", numbered claims | Numbered nested claims. One job per integer. Match statement files already beside the work. Continuous prose is the wrong sample. |

## Idiolect extraction

Voice is not stored in an examples folder and is not a fixed portrait of one writer. It is recovered, at the time of writing, from the text that already surrounds the job: the file being edited, sibling files in the same folder, and any passage the user names or attaches. If those conflict, the named passage wins, then the file in hand, then the nearest sibling.

Treat that corpus as the sole evidence. Do not import a generic "human" style, and do not "correct" the corpus toward standard edited English.

The extraction is a descriptive analysis of an idiolect, not a rewrite of it. Read for recurrent formal features and copy those features. Do not summarize the writer's "personality."

**Graphological and orthographic features.** Spelling that recurs. Agreement that recurs. `its` / `it's` as the corpus actually mixes them. Capitalization, including a mid-sentence lowercase `i` if it is there. Quotation marks: straight or curly, closed or left open. Whether a pause is a comma, a parenthesis, or a dash. Whether backticks are used as homemade term-marks rather than as code. Unclosed quotes and leftover oral grammar stay if they were already there. Idiosyncrasy in the corpus is data. When the source is the user's (mint, reform, clean-up), do not normalize spelling, agreement, or pronoun forms.

**Syntactic features.** Mean and variance of sentence length. Coordination with `and` / `but` versus subordination. Whether a short sentence opens or closes a block, or sits as a slogan in the middle. Tense that slips and stays. Stiff grammar set next to talk (`I knew not…`). Hedges as ordinary asides, after which the sentence continues. Whether a ranking, once started, is walked back in the same breath.

**Lexical features.** Pair-nouns and local terms, named once and then used, not rotated through synonyms. Register jump: a concrete local noun set beside a stiff or technical one, with no gear-change sentence between them. Do not pick "plain" or "philosophical" and stay there. Contractions, fillers, and hedges if the corpus keeps them. Do not upgrade vocabulary.

**Discursive and pragmatic features.** Person: talk *from* I when the corpus does. Direct address is rare unless the corpus uses it. Role-as-camera (`As a parent I…`) is not a lectern "we." How a claim is staged: scene first, question from inside the scene, rather than a definition up front. Analogy as a move — same shape, different field — then one explicit return (`So, back to…`). Distinctions the corpus bothers to name, it names. It does not restate the distinction as a closer. Warmth where the example is small. Dryness where an adult is incompetent. No sermon after the feeling.

**Textual features.** Paragraph length varies with the thought. Subheads and bullets appear only if the surrounding text uses them. Openings sit on hands and place when that is the corpus habit. Endings are quieter than the middle. A short last line may sit slightly balanced. Do not add a moral paragraph after it.

When generating new prose in an extracted voice: copy the grammar moves, the register jump, the marks, and the scene-then-return if those are what the corpus does. Do not spray fake typos as costume. A light echo of a recurrent mark is enough once the syntax and the diction already match. Do not invent fingerprint the corpus does not have.

Continuous-prose features do not transfer into statements. Statement voice is extracted only from other statement files beside the work.

## Statements

This is a separate genre. Do not write conversational ramble, essay paragraphs, or a closer that retells the page.

- Title as `**On x.**` then numbered claims: `1.` / `1.1` / `1.2`. Blank line between items.
- One job per integer. A subpoint specifies (how, at whom, what has no bearing). It does not restate the parent in a new metaphor.
- Keep local nouns already in the surrounding statement files. Name them from those files. Do not import a glossary from elsewhere.
- State the mechanism. Do not single out a faction as the hollow case.
- No kicker after a claim. No contrast engine in numbered form. No punchy break line. No quippy two-beat. No fashion verb standing in for the mechanism.
- No last integer that recaps earlier ones.
- Do not retell one statement file inside another.
- If a line sounds like a slogan, rewrite it in diction already in the surrounding statement files. Ugly and specific beats tidy and punchy.
- Stop when the new claim is on the page.

## Minting speech and rough drafts

- Punctuate, paragraph, and fix obvious homophones. Normalize `its` / `it's` only if the rest of the surrounding text already does.
- Do not upgrade vocabulary. Do not invent a lede, a kicker, or a "so what" they did not say.
- Do not restructure into claim, example, impact, refinement.
- Keep false starts if they are a thought being found. Drop only pure duplicates and mic noise.
- If a stretch is inaudible or nonsense, mark it. Do not smooth it into a polished claim.
- A minted draft should still sound spoken. Stop before it sounds published.

## Translating minted essays

Use this when the source already sounds like writing. A cadence pass will leave the same bones.

1. Make a private point list: claims, examples, names, dates, caveats. No sentences copied from the source. No section titles. No slogans.
2. Mark which items are the argument and which are recap, self-advertisement, or the same metaphor said again.
3. Discard the bones: series recap, "what I haven't done yet," slogan headings, the synthesis closer, the door/map/field ending, the "this is the part that's actually mine" frame.
4. Write from the point list as if thinking it through once, in the extracted voice. New paragraph order is allowed if the thought wants it. New claims are not.
5. Keep one analogy if the source needed it. Do not keep the analogy and the restatement of the analogy and the moral of the analogy.
6. Caveats stay. Write them as ordinary asides, not as a staged confession of intellectual honesty.
7. Stop when the points are on the page. Do not add a "put together" paragraph that retells the piece.

## Reforming slop

Work at the level of rhythm and move, not synonym swaps.

1. Find the actual claim. One claim per stretch. Delete the restatements that only change the metaphor.
2. Break the three-beat unit: setup, illustration, punch. Stop after the thought is clear, or wander. Do not land a slogan.
3. Prefer one slightly too-long sentence over a drumroll of short ones.
4. Keep odd nouns and local diction. If they said a phrase once, do not recast it under three new names.
5. After the pass, read it aloud. If the template is still audible, cut again.

Do not replace one template with another. Concrete-and-terse is still a template if every paragraph does it.

## Banned cadences

Fine once in a rare while. Slop when they recur, or when they are the engine of the paragraph.

**Contrast engines**

- "It's not X, it's Y."
- "This isn't X — it's Y."
- "The question isn't X. The question is Y."
- "X isn't the exception. It's the rule."
- "Not because A. Because B."
- "That doesn't just ____. It ____."
- "It doesn't merely / simply / only X. It Y."

**Three-beat sermon**

- Claim with example. Impact sentence. Sharp refinement.
- Short kicker after a long sentence, every time: "That is the whole relation." "It is not." "That is the point."
- Mid-claim landing beat: a short verdict dropped between two longer sentences so the paragraph can nod. "Ordinary life already runs on it." "We accept this without question." "And that is the whole of it." The claim was already said. The short line only congratulates it. Cut it. Do not move it to the end.
- Narrator-in-the-argument: the claim is turned into a place, and the writer walks through it. "I leave the stretch where I can point." "Follow it far enough and." "Run it back and I arrive at." "I cannot find the edge where this stops and something else begins." "That is the situation in." "The miss that follows from." The corpus states a relation between things. It does not stage a journey toward the relation, and it does not build a landscape (stretch, edge, gap-as-place, far enough) for that journey to happen in. If the sentence needs a verb of travel to reach the claim, the claim is not yet written. Write the relation. Delete the trip.
- Anaphora stacks: "It's about X. It's about Y. It's about Z."
- Rule of three used as architecture instead of accident.

**Essay-bot glue**

- "Here's the thing." "Let's unpack." "Let that sink in." "Read that again." "And that changes everything."
- "At its core." "In a very real sense." "When you think about it."
- "What's at stake is." "The real X is." "One thing is clear."
- "From X to Y." "Whether X or Y." "In a world where."
- Paragraph-start "Moreover / Furthermore / Additionally / Ultimately / Importantly."

**Inflated diction.** See the living list. Do not "fix" a banned word by swapping in another word from the same list.

**Essay architecture.** Page-level templates. A sentence ban will not catch them. If the source is built this way, translate. Do not reform.

- Series recap as the lede: tour of prior essays, then "what I haven't done yet," then the question that "actually matters."
- Slogan subheads that announce the move.
- One metaphor run as a machine: introduce it, apply it, restate it as "if that's right," then a kicker that only restates the metaphor.
- Self-advertising frames: "the harder claim," "the part I think is actually mine," "rather than just a repackaging," "I want to flag something here rather than bury it."
- Disclaimer sandwich: "I'm not claiming A, or B, or C. I'm claiming D."
- Parallel institution list as proof, each item a mini-sermon, then "that's what compounding X looks like."
- Synthesis closer: "Put together:" / a door, map, or field ending / fingerprints listed in threes / "not because the field was crowded."
- Even, oratorical paragraphs that all end on a verdict. No leftover oral grammar. No short ugly aside.

**Punctuation tics**

- Em dashes as drama. A pair of asides is fine. Three fake-oral dashes on a page is not.
- Every heading a parallel slogan.
- Perfectly even paragraph lengths, each closing on a moral.

## Banned words and phrases

Hard ban in model-written prose unless the user already used that exact word in the source, the surrounding text, or an explicit keep-this note. Cadence bans are about shape. This list is about fashion. New models mint new fashion. Keep the list ugly and current.

**How to update**

- User flags a word or phrase: append it under the right heading, one bullet, no commentary.
- Do not delete old entries. Dead models still leak. Sort only if the user asks.
- If they say a word is fine in a specific piece, that piece only. Do not remove it from the list.
- Prefer the dumb literal over a clever rewrite of the ban. The next model has to grep this.
- When in doubt which heading, put it under current-model fashion.

### Current-model fashion

- load-bearing
- through-line / throughline
- the quiet X / the quiet part
- scaffolding (metaphorical)
- texture / the grain of (as fake depth)
- interstitial / liminal
- palimpsest
- braid / braided (as essay structure)
- metabolize / metabolizes (ideas, not food)
- freighted / charged (as in "a charged term")
- hinge / the hinge of the argument
- ballast / spine of the argument
- north star
- blast radius / surface area (as idea-talk)
- receipts / the receipts
- steelman / steel-man
- "doing a lot of work" / "does the work" / "the work of"
- "this is the move" / "the move here"
- "what's doing the work"
- "worth sitting with" / "sit with" / "stay with"
- "I want to be careful here" / "it's worth being precise"
- "the charitable reading"
- "names" / "what this is naming" (as a verb for analysis)
- "earns" / "doesn't earn" / "has to earn" (applied to sentences, claims, endings)
- "lands" / "doesn't land" (same)
- already runs on it / ordinary life already
- leave the stretch / the stretch where
- follow far enough / run it back far enough
- I cannot find the edge where
- it still runs
- it still lands
- how it lands / where it lands / etc.
- still holds / still obtains
- "and it still X" (kicker after a claim)
- "that move is easier to hear"
- "not choosing is still a choice"
- "X.XX states that" / "X.XX says" / "X.XX already said" / "X.XX has a name for" / "X.XX just named" / "X.XX wants" (a numbered claim made the subject of a reporting verb; the number goes in the clause or in parentheses, it does not narrate)
- reprinting a numbered claim as a lede / opening with another number's wording
- "A gap is not, by itself, a lie" / "the gap being, by itself, a lie"

### Evergreen assistant diction

- delve, tapestry, landscape (metaphorical), nuanced, multifaceted
- pivotal, crucial, robust, vibrant, noteworthy, compelling
- underscore, foster, showcase, leverage, utilize, facilitate
- navigate / navigating (metaphorical), journey (metaphorical)
- unpack, deep dive / deep-dive
- "stands as a testament" / "serves as" / "is a reminder that"
- "speaks to" / "speaks volumes" / "a masterclass in" / "a case study in"
- "in a world where" / "at the end of the day" / "the reality is" / "the truth is"
- "cannot be overstated" / "nothing short of" / "in no small part"
- "make no mistake" / "needless to say" / "it goes without saying"
- "simply put" / "to put it simply" / "in other words" / "put differently" / "said another way"
- "it's tempting to" / "it's easy to" / "one might object"
- Fake-weight fragments: "Period." "Full stop." "Exactly." "Indeed."

## What to write instead

- Name the object. Then say what it does. Stop.
- Let a sentence be ugly if the thought is unfinished.
- Vary paragraph length for the thought, not for pulse.
- Use "I" when the source is first-person. Do not smuggle a lectern "we."
- In fiction, stay on hands, tools, light, jobs, and what people refuse to say. Do not editorialize the theme in the last line of a beat.
- One metaphor per idea. Do not rotate synonyms of the same metaphor to fake depth.

## Self-check

Before showing prose:

- Could a reader mark three "not X, Y" turns without hunting? Cut two.
- Does every paragraph end with a verdict? Open or lower some endings.
- Did you add a sentence whose only job is impact? Delete it.
- Does the page still have a recap lede, slogan subheads, and a "put together" closer? That is leftover bones. Translate again. Do not nibble.
- Would this pass as a continuation of the surrounding text? If not, rewrite toward that text, not toward "better English."
- Matching continuous prose: did you open with a definition the corpus does not open with, lock one register, dash-ify pauses the corpus marks with commas, or "fix" their spelling? Wrong.
- Writing a statement? The sample is the other statement files, not the continuous prose. No kicker after the claim. No recap integer.
- Search the living list against the draft. One hit is already too many unless it was the user's word.