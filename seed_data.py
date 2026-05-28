"""Run once to populate the database with laws, case stories, and scenario guides."""
import json
from app import app, db, Category, Law, CaseStory, Guide

with app.app_context():
    db.drop_all()
    db.create_all()

    # ── Categories ───────────────────────────────────────────────────────────────
    housing = Category(slug="housing", name="Housing & Renting", icon="",
        description="Evictions, repairs, deposits, and tenant rights.")
    police = Category(slug="police", name="Police & Your Rights", icon="️",
        description="What to do when stopped, arrested, or searched.")
    family = Category(slug="family", name="Family", icon="️",
        description="Custody, child support, and domestic violence.")
    work = Category(slug="work", name="Work & Money", icon="",
        description="Unpaid wages, firing, debt collectors.")

    db.session.add_all([housing, police, family, work])
    db.session.flush()

    # ── Housing Laws ──────────────────────────────────────────────────────────────
    db.session.add(Law(
        category_id=housing.id,
        title="My Landlord Won't Fix My Home",
        statute="Alabama Code § 35-9A-204",
        legal_text=(
            "The landlord shall maintain the premises in a habitable condition, "
            "including heat, running water, and working plumbing and electrical systems."
        ),
        plain_english=(
            "Your landlord MUST keep your home safe and working. "
            "That means hot water, heat in winter, a roof that doesn't leak, "
            "and working toilets. If they don't fix these things, you have rights."
        ),
        steps=json.dumps([
            "Write a letter (or text) to your landlord listing exactly what is broken.",
            "Keep a copy of that letter — a screenshot of a text counts.",
            "Give them 14 days to fix the problem.",
            "If they don't fix it, call your local housing authority or a Legal Aid office.",
        ]),
        consequences=json.dumps([
            "Landlord can be ordered to pay you back rent if the home was unlivable.",
            "Landlord may owe you money for moving costs if you had to leave.",
            "In serious cases, the city can condemn the building.",
        ]),
        warning=(
            "Do NOT just stop paying rent. In Alabama you can still be evicted "
            "even if the house is broken. You MUST send the letter first."
        ),
        keywords="repair,fix,broken,heat,water,plumbing,roof,landlord,habitable,maintenance",
    ))
    db.session.add(Law(
        category_id=housing.id,
        title="My Landlord Is Trying to Evict Me",
        statute="Alabama Code § 35-9A-401",
        legal_text=(
            "A landlord shall not remove a tenant from the premises or cut off "
            "utilities without going through the court eviction process."
        ),
        plain_english=(
            "Your landlord cannot just change your locks or turn off your power "
            "to force you out. They MUST go to court first. "
            "If they do it without a court order, that is illegal."
        ),
        steps=json.dumps([
            "If your landlord locks you out illegally, call the police — it is a crime.",
            "If you get an eviction notice, you usually have 7 days to pay rent or leave.",
            "You can go to court and tell your side of the story.",
            "Contact Legal Aid Alabama (1-866-456-4995) for free help.",
        ]),
        consequences=json.dumps([
            "Landlord who illegally locks you out can be sued.",
            "You may be able to stay in your home while the case is in court.",
            "If you lose in court, a sheriff will give you a set number of days to move.",
        ]),
        warning=(
            "If you receive official court papers, do NOT ignore them. "
            "Missing a court date almost always means you lose automatically."
        ),
        keywords="eviction,evict,lock out,lockout,kicked out,notice,court,utilities",
    ))
    db.session.add(Law(
        category_id=housing.id,
        title="Getting My Security Deposit Back",
        statute="Alabama Code § 35-9A-201",
        legal_text=(
            "Upon termination of the tenancy, the landlord shall return the security "
            "deposit within 60 days, with an itemized written statement of any deductions."
        ),
        plain_english=(
            "When you move out, your landlord has 60 days to either give back your deposit "
            "or send you a written list of what they took money for. "
            "Normal wear-and-tear (small scuffs, faded paint) does NOT count as damage."
        ),
        steps=json.dumps([
            "Take photos of every room the day you move out.",
            "Return all keys and get proof you returned them.",
            "Send your landlord your new address in writing.",
            "If 60 days pass with no response, you can sue in small claims court.",
        ]),
        consequences=json.dumps([
            "If your landlord keeps your deposit without a reason, you can sue for the full amount.",
            "Small claims court in Alabama handles cases up to $6,000.",
            "You do not need a lawyer for small claims court.",
        ]),
        warning=None,
        keywords="deposit,security deposit,move out,refund,deduction,small claims",
    ))

    # ── Police Laws ───────────────────────────────────────────────────────────────
    db.session.add(Law(
        category_id=police.id,
        title="What To Do If Police Stop You on the Street",
        statute="4th & 5th Amendments (U.S. Constitution) + Terry v. Ohio",
        legal_text=(
            "Officers may briefly detain a person if they have reasonable articulable "
            "suspicion of criminal activity. You have the right to remain silent."
        ),
        plain_english=(
            "A police officer CAN stop and ask you questions. "
            "You do NOT have to answer most questions, but you should stay calm. "
            "In Alabama you must give your name if asked during a lawful stop."
        ),
        steps=json.dumps([
            "Stay calm. Keep your hands where the officer can see them.",
            "Say clearly: 'I am invoking my right to remain silent.'",
            "You must give your name in Alabama if asked during a stop.",
            "Do NOT run. Do NOT touch the officer.",
            "If you are free to go, ask calmly: 'Am I being detained or am I free to go?'",
            "Write down or record everything you remember right after.",
        ]),
        consequences=json.dumps([
            "Refusing to identify yourself during a lawful detention is a Class C misdemeanor.",
            "Resisting arrest — even if the arrest is wrong — can lead to extra charges.",
            "You can file a complaint with the police department's internal affairs afterward.",
        ]),
        warning=(
            "Do NOT argue about whether the stop is legal on the street. "
            "Fight it in court later — it is much safer."
        ),
        keywords="police,stop,detained,arrest,rights,remain silent,search,officer,street",
    ))
    db.session.add(Law(
        category_id=police.id,
        title="Can Police Search My Car or Home?",
        statute="4th Amendment (U.S. Constitution)",
        legal_text=(
            "The right of the people to be secure in their persons, houses, papers, "
            "and effects, against unreasonable searches and seizures, shall not be violated."
        ),
        plain_english=(
            "Police generally need a WARRANT (a judge's permission) to search your home. "
            "For your car, they need a warrant OR a reason to believe there is evidence of a crime. "
            "You can say no — but do it calmly and in words only."
        ),
        steps=json.dumps([
            "Calmly say: 'I do not consent to a search.'",
            "Do NOT physically block or touch the officer.",
            "If they search anyway, do not resist — let a court decide later.",
            "Write down the officer's name and badge number afterward.",
        ]),
        consequences=json.dumps([
            "Evidence found in an illegal search may be thrown out of court.",
            "If you consent to a search, anything found can be used against you.",
        ]),
        warning=(
            "Saying 'I do not consent' does NOT mean police will stop searching. "
            "It protects your rights in court later."
        ),
        keywords="search,warrant,car,home,house,consent,seizure,fourth amendment",
    ))

    # ── Family Laws ───────────────────────────────────────────────────────────────
    db.session.add(Law(
        category_id=family.id,
        title="Child Custody: Who Gets the Kids?",
        statute="Alabama Code § 30-3-152",
        legal_text=(
            "The court shall make a custody determination based on the best interest "
            "of the child, considering all relevant factors."
        ),
        plain_english=(
            "In Alabama, a judge decides where children live based on what is best FOR THE CHILD — "
            "not which parent 'wins.' Both parents usually get some time with their children "
            "unless there is abuse or danger."
        ),
        steps=json.dumps([
            "Write down dates and examples of your involvement in your child's life.",
            "Keep records: school pickups, doctor visits, activities you attend.",
            "If there is domestic violence, tell the court — it matters.",
            "You can ask the court for a custody arrangement even without a lawyer.",
        ]),
        consequences=json.dumps([
            "Violating a custody order can result in fines or jail time.",
            "Keeping a child from the other parent without a court order can hurt your case.",
            "Courts look at who has been the main caregiver up to that point.",
        ]),
        warning=(
            "Do NOT take your child out of state without the other parent's agreement "
            "or a court order. This can be considered parental abduction."
        ),
        keywords="custody,child,kids,divorce,parent,visitation,court,best interest",
    ))
    db.session.add(Law(
        category_id=family.id,
        title="My Partner Is Hurting Me — What Can I Do?",
        statute="Alabama Code § 30-5-2",
        legal_text=(
            "Any person who is a victim of domestic violence may petition the court "
            "for a Protection from Abuse (PFA) order."
        ),
        plain_english=(
            "If someone in your home is hurting you or threatening you, "
            "you can ask a judge for a Protection from Abuse (PFA) order. "
            "This is a court order that tells the other person to stay away from you. "
            "You do NOT need a lawyer to file."
        ),
        steps=json.dumps([
            "Go to your local courthouse and ask for a PFA form — it is free.",
            "You can get an emergency order the same day if you are in danger.",
            "The order can make them leave the house, even if it is their name on the lease.",
            "Call the Alabama Domestic Violence Hotline: 1-800-650-6522 (free, 24/7).",
        ]),
        consequences=json.dumps([
            "Violating a PFA order is a crime — the police can arrest the other person.",
            "The order can last up to 1 year and be renewed.",
            "A permanent order can affect custody and divorce proceedings.",
        ]),
        warning=(
            "It is safest to have a safety plan before telling your partner you are filing. "
            "The hotline can help you plan safely."
        ),
        keywords="domestic violence,abuse,hurt,protection,PFA,restraining order,partner,spouse,safe",
    ))

    # ── Work Laws ─────────────────────────────────────────────────────────────────
    db.session.add(Law(
        category_id=work.id,
        title="My Boss Didn't Pay Me",
        statute="Alabama Code § 25-3-2 + Fair Labor Standards Act",
        legal_text=(
            "Every employer shall pay each employee all wages due on regular paydays "
            "designated in advance. Federal law requires minimum wage of $7.25/hour."
        ),
        plain_english=(
            "Your boss is REQUIRED to pay you every penny you earned. "
            "If they don't pay you — including your last check — that is wage theft "
            "and it is against the law. The minimum wage in Alabama is $7.25/hour."
        ),
        steps=json.dumps([
            "Gather evidence: pay stubs, timecards, texts, screenshots, bank records.",
            "Write your employer a letter asking for the money owed.",
            "File a complaint with the Alabama Department of Labor: (334) 242-3460.",
            "File a federal complaint with the U.S. Department of Labor Wage and Hour Division (free).",
        ]),
        consequences=json.dumps([
            "Your employer can be ordered to pay double what they owe you (called 'liquidated damages').",
            "You can also sue in court — you do not need to pay to file a DOL complaint.",
            "Retaliation (firing you for complaining) is also illegal.",
        ]),
        warning=None,
        keywords="wages,pay,unpaid,paycheck,fired,last check,wage theft,boss,employer,minimum wage",
    ))
    db.session.add(Law(
        category_id=work.id,
        title="A Debt Collector Keeps Calling Me",
        statute="Fair Debt Collection Practices Act (FDCPA)",
        legal_text=(
            "A debt collector may not engage in any conduct the natural consequence "
            "of which is to harass, oppress, or abuse any person."
        ),
        plain_english=(
            "Debt collectors CANNOT call you before 8 AM or after 9 PM. "
            "They cannot threaten you, lie to you, or call you at work if you tell them to stop. "
            "If they do any of these things, THEY are breaking the law."
        ),
        steps=json.dumps([
            "Write a letter telling them to stop contacting you — by law they must stop.",
            "Ask them to send you proof of the debt in writing (within 30 days of first contact).",
            "Keep a log of every call: date, time, what was said.",
            "Report them to the Consumer Financial Protection Bureau (CFPB) at consumerfinance.gov.",
        ]),
        consequences=json.dumps([
            "You can sue a debt collector who breaks these rules for up to $1,000 per violation.",
            "They must pay your attorney fees if you win.",
            "Filing a CFPB complaint is free.",
        ]),
        warning=(
            "Writing to stop contact does NOT make the debt go away. "
            "But it does give you peace and time to figure out your options."
        ),
        keywords="debt,collector,calls,harass,phone,owe,collection,credit,bills",
    ))

    db.session.flush()

    # ── Case Stories ──────────────────────────────────────────────────────────────
    db.session.add(CaseStory(
        category_id=work.id,
        summary="A worker in Mobile said their boss didn't pay them for their last two weeks of work.",
        year=2021, location="Mobile, AL",
        outcome="The worker won their case with the Alabama Department of Labor because they had saved photos of their timecards and screenshots of texts where their boss promised to pay.",
        follow_up_question="Do you have photos of your timecards, pay stubs, or any texts about your pay?",
        keywords="wages,pay,unpaid,paycheck,last check,work,boss,timecard",
    ))
    db.session.add(CaseStory(
        category_id=housing.id,
        summary="A renter in Birmingham said their landlord refused to fix a broken heater for two months in winter.",
        year=2022, location="Birmingham, AL",
        outcome="After the tenant sent a certified letter and the landlord still did not respond, Legal Aid Alabama helped them break the lease without penalty and recover one month's rent.",
        follow_up_question="Did you send your landlord a written notice (text, letter, or email) about the repair?",
        keywords="repair,heat,heater,broken,landlord,fix,winter,habitability,lease",
    ))
    db.session.add(CaseStory(
        category_id=housing.id,
        summary="A tenant in Huntsville was locked out of their apartment by the landlord without a court order.",
        year=2023, location="Huntsville, AL",
        outcome="The tenant called police who verified it was an illegal lockout. The tenant was let back in the same night and later won a civil case for damages.",
        follow_up_question="Did your landlord change the locks or remove your belongings without a court eviction order?",
        keywords="lockout,lock out,eviction,illegal,apartment,landlord,kicked out",
    ))
    db.session.add(CaseStory(
        category_id=work.id,
        summary="A fast-food worker in Montgomery was paid less than minimum wage and never received overtime.",
        year=2023, location="Montgomery, AL",
        outcome="After filing with the U.S. Department of Labor, the worker received back pay plus an equal amount in damages — totaling almost $4,000.",
        follow_up_question="Do you have any pay stubs or records showing your hourly rate and hours worked?",
        keywords="minimum wage,overtime,pay,wages,fast food,restaurant,underpaid",
    ))
    db.session.add(CaseStory(
        category_id=family.id,
        summary="A parent in Tuscaloosa said the other parent took their child and wouldn't allow visits.",
        year=2022, location="Tuscaloosa, AL",
        outcome="The parent filed an emergency custody petition. Because they had documented their involvement (school records, photos, texts), the court granted them interim visitation within two weeks.",
        follow_up_question="Do you have records showing your involvement in your child's life — school records, photos, receipts?",
        keywords="custody,child,visits,visitation,parent,taken,denied,access",
    ))

    db.session.flush()

    # ════════════════════════════════════════════════════════════════════════
    # Pillar 2 — Scenario Guides
    # ════════════════════════════════════════════════════════════════════════

    # ── Guide 1: Security Deposit Recovery ───────────────────────────────────
    db.session.add(Guide(
        category_id=housing.id,
        slug="security-deposit",
        title="Security Deposit Recovery",
        subtitle="Get your deposit back after moving out",
        icon="",
        scenario="You moved out of your rental and your landlord is refusing to return your security deposit, or is making deductions you think are unfair.",
        timeline=json.dumps([
            {"day": "Move-out day", "label": "Take photos of every room, return keys, get signed confirmation."},
            {"day": "Day 1–3", "label": "Send landlord your new address in writing (text or letter)."},
            {"day": "Day 60", "label": "Alabama law: landlord must return deposit OR send itemized deductions by this date."},
            {"day": "Day 61+", "label": "If no deposit and no letter, you can sue in small claims court."},
        ]),
        checklist=json.dumps([
            {"text": "Photograph every room before leaving", "tip": "Date-stamp photos on your phone. Do this the same hour you hand over keys."},
            {"text": "Return all keys and get written confirmation", "tip": "A text reply from your landlord saying 'got the keys' counts."},
            {"text": "Send your new mailing address in writing", "tip": "Screenshot the text or email so you have proof you sent it."},
            {"text": "Wait up to 60 days from move-out", "tip": "Alabama law gives landlords 60 days to act."},
            {"text": "Review any itemized deduction letter", "tip": "Normal wear (scuffs, faded paint) is NOT chargeable damage."},
            {"text": "Send a formal demand letter if deposit is withheld unfairly", "tip": "Use the 'Generate Letter' button below.", "action": "letter"},
            {"text": "File in small claims court if no response", "tip": "Alabama small claims handles up to $6,000. No lawyer needed.", "warning": "File within 6 years of move-out."},
        ]),
        letter_template="""[Your Full Name]
[Your Current Address]
[City, State, ZIP]
[Date]

[Landlord's Full Name]
[Landlord's Address]
[City, State, ZIP]

Re: Demand for Return of Security Deposit — [Property Address]

Dear [Landlord's Name],

I am writing to formally request the return of my security deposit of $[Amount] for the rental property located at [Property Address], from which I vacated on [Move-Out Date].

Under Alabama Code § 35-9A-201, you are required to return my deposit or provide an itemized written statement of deductions within 60 days of the termination of my tenancy. As of [Today's Date], I have not received either.

I maintained the property in good condition, as documented by photos taken on my move-out date. Any deductions for normal wear-and-tear are not permitted under Alabama law.

I request that you return the full deposit of $[Amount] within 14 days of receiving this letter. If I do not receive a response, I will pursue this matter in small claims court, where I may be entitled to recover the full deposit amount plus court costs.

Please send the deposit to my current address listed above.

Sincerely,
[Your Full Name]
[Your Phone Number]
[Your Email]""",
        keywords="deposit,security deposit,move out,refund,small claims,deduction",
    ))

    # ── Guide 2: Unpaid Wages ─────────────────────────────────────────────────
    db.session.add(Guide(
        category_id=work.id,
        slug="unpaid-wages",
        title="Recovering Unpaid Wages",
        subtitle="When your employer won't pay you what you earned",
        icon="",
        scenario="Your employer owes you wages — whether it's your final paycheck, overtime pay, or hours they claim they didn't track.",
        timeline=json.dumps([
            {"day": "As soon as possible", "label": "Gather all evidence of hours worked and pay promised."},
            {"day": "Week 1", "label": "Send employer a written demand for the unpaid wages."},
            {"day": "Week 2–3", "label": "File complaint with Alabama Dept. of Labor or U.S. DOL Wage & Hour Division."},
            {"day": "2 years", "label": "Federal deadline (FLSA statute of limitations) to file a claim for unpaid wages."},
        ]),
        checklist=json.dumps([
            {"text": "Write down all dates and hours you worked", "tip": "Include start/end times for every shift, even from memory."},
            {"text": "Collect all pay stubs, bank deposit records, or cash receipts", "tip": "Even screenshots of Venmo/CashApp payments count."},
            {"text": "Save texts, emails, or app messages about your pay or hours", "tip": "Screenshot everything — employers sometimes delete records."},
            {"text": "Note the exact amount you are owed and why", "tip": "Be specific: '$320 for 40 hours of work at $8/hr the week of June 3.'"},
            {"text": "Send a written demand letter to your employer", "tip": "Use the 'Generate Letter' button below.", "action": "letter"},
            {"text": "File a free complaint with the U.S. DOL Wage & Hour Division", "tip": "Visit dol.gov/agencies/whd or call 1-866-4-US-WAGE. No lawyer needed."},
            {"text": "Know that retaliation is illegal", "tip": "Your employer cannot legally fire or punish you for filing a complaint.", "warning": "Document any retaliation immediately."},
        ]),
        letter_template="""[Your Full Name]
[Your Address]
[City, State, ZIP]
[Date]

[Employer / Manager Name]
[Company Name]
[Company Address]

Re: Formal Demand for Unpaid Wages

Dear [Employer Name],

I am writing to formally request payment of wages I am owed for work performed at [Company Name].

I worked [Number of Hours] hours during the period of [Start Date] to [End Date] at a rate of $[Hourly Rate] per hour, totaling $[Total Amount Owed]. As of [Today's Date], I have not received this payment.

Under the Fair Labor Standards Act (FLSA) and Alabama wage law, employers are required to pay all earned wages promptly. Failure to do so constitutes wage theft and may result in legal action including double damages.

I request payment of the full amount of $[Total Amount Owed] within 7 days of receiving this letter.

If payment is not received, I will file a formal complaint with the U.S. Department of Labor's Wage and Hour Division and pursue all available legal remedies.

Sincerely,
[Your Full Name]
[Your Phone Number]
[Your Email]""",
        keywords="wages,unpaid,paycheck,overtime,employer,boss,work,hours",
    ))

    # ── Guide 3: Fighting an Eviction ─────────────────────────────────────────
    db.session.add(Guide(
        category_id=housing.id,
        slug="fight-eviction",
        title="Fighting an Eviction Notice",
        subtitle="Understand your rights and respond to an eviction",
        icon="",
        scenario="You received an eviction notice from your landlord and need to understand what it means and how to respond.",
        timeline=json.dumps([
            {"day": "Day 0", "label": "You receive an eviction notice. Read it carefully — note the exact date and reason."},
            {"day": "Day 1–3", "label": "Determine the type: non-payment of rent (7 days to cure) or lease violation (varies)."},
            {"day": "Day 3–5", "label": "Contact Legal Aid Alabama (1-866-456-4995). They may be able to help for free."},
            {"day": "Court date", "label": "Appear in court even if you think you'll lose. Not showing up = automatic loss."},
        ]),
        checklist=json.dumps([
            {"text": "Read the notice carefully — note the reason and deadline", "tip": "The notice must state a legal reason. 'I don't like you' is not a legal reason."},
            {"text": "Check if the notice was delivered correctly", "tip": "Alabama law requires proper service — hand-delivered or posted + mailed."},
            {"text": "Gather your lease, payment receipts, and any communications", "tip": "Bank records and transfer screenshots prove you paid rent."},
            {"text": "If for non-payment: try to pay in full within the 7-day window", "tip": "Paying in full can stop the eviction before court."},
            {"text": "Contact Legal Aid Alabama for free help", "tip": "Call 1-866-456-4995. They handle eviction cases for free or low-cost."},
            {"text": "Respond in writing to your landlord if you dispute the reason", "tip": "Use the 'Generate Letter' button below.", "action": "letter"},
            {"text": "Appear at every court date", "tip": "Missing court = automatic judgment against you.", "warning": "Mark your court date in your phone NOW."},
        ]),
        letter_template="""[Your Full Name]
[Your Address]
[City, State, ZIP]
[Date]

[Landlord / Property Manager Name]
[Landlord Address]

Re: Response to Eviction Notice Dated [Notice Date] — [Property Address]

Dear [Landlord Name],

I am writing in response to the eviction notice I received on [Date Received], regarding the property at [Property Address].

[Choose one of the following and delete the others:]

OPTION A — Disputing non-payment:
I dispute the claim that I owe unpaid rent. Enclosed/attached are my payment records showing rent was paid on [dates]. I request that you confirm receipt and withdraw this notice.

OPTION B — Disputing a lease violation:
I dispute the alleged lease violation stated in the notice. [Briefly explain why the claim is incorrect.] I am committed to maintaining the property in accordance with our lease agreement.

OPTION C — Requesting additional time:
I acknowledge the notice and am actively working to resolve this matter. I respectfully request [number] additional days to [pay/remedy the situation] and am willing to discuss a payment plan.

I ask that we resolve this matter without court proceedings. Please contact me at [phone/email] to discuss.

Sincerely,
[Your Full Name]
[Your Phone Number]""",
        keywords="eviction,notice,court,rent,landlord,dispute,lease",
    ))

    # ── Guide 4: Freelance Contract Dispute ──────────────────────────────────
    db.session.add(Guide(
        category_id=work.id,
        slug="freelance-dispute",
        title="Freelance Contract Dispute",
        subtitle="When a client won't pay for work you completed",
        icon="",
        scenario="You completed freelance or contract work and the client is refusing to pay, delaying payment, or disputing the amount owed.",
        timeline=json.dumps([
            {"day": "Immediately", "label": "Document all completed work: files delivered, emails, messages, invoices."},
            {"day": "Day 1–7", "label": "Send a formal payment demand with a 7–14 day deadline."},
            {"day": "Day 14–30", "label": "If no payment, file in small claims court (up to $6,000 in Alabama)."},
            {"day": "4–6 years", "label": "Alabama statute of limitations for breach of written contract."},
        ]),
        checklist=json.dumps([
            {"text": "Locate your contract or written agreement", "tip": "Even an email confirming the job scope and rate counts as a contract."},
            {"text": "Document all work delivered", "tip": "Save file delivery emails, download confirmations, finished work copies."},
            {"text": "Save all communication about the project", "tip": "Screenshots of texts, Slack, email threads — all are evidence."},
            {"text": "Calculate the exact amount owed", "tip": "Include your rate, hours/deliverables, and any agreed expenses."},
            {"text": "Send a formal demand letter via email and certified mail", "tip": "Use the 'Generate Letter' button below.", "action": "letter"},
            {"text": "File in small claims court if payment is under $6,000", "tip": "Alabama small claims is fast, cheap, and you don't need a lawyer."},
            {"text": "Consider a collections agency for larger amounts", "tip": "They take a percentage but handle the recovery for you."},
        ]),
        letter_template="""[Your Full Name / Business Name]
[Your Address]
[City, State, ZIP]
[Date]

[Client Name / Company]
[Client Address]

Re: Formal Demand for Payment — Invoice #[Invoice Number]

Dear [Client Name],

This letter is a formal demand for payment of $[Amount] for services rendered under our agreement dated [Contract Date].

I completed all contracted deliverables as specified, including [brief description of work], which were delivered on [Delivery Date]. As of [Today's Date], payment has not been received despite [prior reminders / the payment deadline of X passing].

Per our agreement, payment of $[Amount] was due on [Due Date]. This amount is now [X days] overdue.

I request payment in full within 14 days of this letter. If payment is not received by [Deadline Date], I will pursue this matter in small claims court and seek recovery of the full amount plus filing fees and interest.

Please remit payment to [Payment Method / Address] or contact me at [phone/email] to resolve this matter.

Sincerely,
[Your Full Name]
[Your Business Name, if applicable]
[Your Phone Number]
[Your Email]""",
        keywords="freelance,contract,client,unpaid,invoice,dispute,work,payment",
    ))

    db.session.commit()
    print(" Database seeded with laws, case stories, and 4 scenario guides.")
