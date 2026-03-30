# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

So the uml design is for a standard CRUD scheduler. We're starting bottom up, ownership of the task is the pet. pet is the owner. then owner is the scheduler. This allows for a natural hierarchy where each parent can have multiple children all the way down. 

Scheduler - assigned responsibilities having to do with timing, conflicts, scheduling. 

Owner - assigned responsibilities regarding pet ownership.

pets - assigned responsibilities regarding tasks and identity of the pet. 

tasks - assigned responsibilities regarding task information, priority, frequency, etc.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?


So for constraints the primary constraint had to be time. we organize by chronological order, earliest first. 
priority stored on every task but we defer to time for sorting currently. I decided on time as the primary constraint because when you're looking at a schedule, it only makes sense to organize chronologically first, but I also added an option to sort by priority as well. 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler had to choose between priority first or time first. we ended up being able to do both, but the primary view is time based. I think it's reasonable because for information, time is more immediately useful for a scheduling app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was extremely helpful in getting situated, distilling instructions down to the most fundamental and important sequence, keeping track of requirements that I had forgotten about, acting as a good reference for the instructions, etc. 

First, I identified the most likely structure of the final project required, then I discussed with the AI the best steps to get to that final structure. I attempted to bypass any pain points by seeing what the final project would look like, and working backwards from there, rather than just slapping on requirements as we went. 

The most useful prompts were questions regarding implementations, and using questions to help lead the AI to the final design of the project/intended use cases of the classes.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One ai design suggestion I pushed back on was not showing completed tasks. completed tasks are useful for a variety of reasons, so I modified the suggestion to add a boolean field to the task, and adding a different ui styling for completed events. it's useful to see completed events for a multitude of reasons, including verification of systems working, and gamification within the app itself - people like feeling like they're accomplishing something. 

I evaluated it by asking my AI to provide code diffs, and following chains of logic to determine which design decisions were related to which parts of the code. Then I asked for an explanation of that specific part.

---



## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
