import streamlit as st
import pandas as pd

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
	page_title="PE Translator",
	page_icon="🎯",
	layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("sample_posts.csv")

# =====================================================
# THEME CLASSIFIER
# =====================================================

def classify_theme(text):

	text = str(text).lower()

	if any(word in text for word in [
    	"insurance","coverage","approval",
    	"copay","denied","refill"
	]):
    	return "Access & Reimbursement"

	elif any(word in text for word in [
    	"diagnosis","diagnosed",
    	"doctor","genetic testing"
	]):
    	return "Diagnosis Journey"

	elif any(word in text for word in [
    	"nausea","side effect",
    	"reaction","stomach"
	]):
    	return "Treatment Limitations"

	elif any(word in text for word in [
    	"orladeyo","treatment",
    	"medication","attacks"
	]):
    	return "Treatment Experience"

	elif any(word in text for word in [
    	"daughter","caregiver",
    	"family","parent"
	]):
    	return "Caregiver Burden"

	else:
    	return "Other"

# =====================================================
# UNMET NEED CLASSIFIER
# =====================================================

def classify_unmet_need(text):

	text = str(text).lower()

	if any(word in text for word in [
    	"insurance","coverage",
    	"approval","copay","denied"
	]):
    	return "Access Barriers"

	elif any(word in text for word in [
    	"diagnosis","diagnosed",
    	"doctor","genetic testing"
	]):
    	return "Healthcare System Friction"

	elif any(word in text for word in [
    	"daughter","caregiver",
    	"family","parent"
	]):
    	return "Emotional Burden"

	elif any(word in text for word in [
    	"nausea","side effect",
    	"stomach","reaction"
	]):
    	return "Treatment Limitations"

	else:
    	return "Further Review Needed"

# =====================================================
# PE OPPORTUNITIES
# =====================================================

def get_opportunity(unmet_need):

	mapping = {

    	"Access Barriers":
        	"Access Support & Navigation",

    	"Healthcare System Friction":
        	"Diagnosis Awareness",

    	"Emotional Burden":
        	"Caregiver Support",

    	"Treatment Limitations":
        	"Treatment Education"
	}

	return mapping.get(
    	unmet_need,
    	"Further Review Needed"
	)

# =====================================================
# RECOMMENDATIONS
# =====================================================

def get_recommendations(unmet_need):

	recommendations = {

    	"Access Barriers": [
        	"Provide reimbursement education resources",
        	"Create access-focused support materials",
        	"Address common insurance questions"
    	],

    	"Healthcare System Friction": [
        	"Increase disease awareness initiatives",
        	"Develop diagnosis journey resources",
        	"Create provider education materials"
    	],

    	"Emotional Burden": [
        	"Expand caregiver support programming",
        	"Create community storytelling opportunities",
        	"Support peer-to-peer engagement"
    	],

    	"Treatment Limitations": [
        	"Gather patient treatment feedback",
        	"Develop expectation-setting resources",
        	"Address treatment burden concerns"
    	]
	}

	return recommendations.get(
    	unmet_need,
    	["Further review needed"]
	)

# =====================================================
# PRIORITY SCORING
# =====================================================

def get_priority(count):

	if count >= 8:
    	return "🔴 High"

	elif count >= 4:
    	return "🟡 Medium"

	else:
    	return "🟢 Opportunity"

# =====================================================
# CREATE COLUMNS
# =====================================================

df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)

# =====================================================
# PAGE HEADER
# =====================================================

st.title("🎯 Patient Engagement Translator")

st.caption(
	"Transforms social listening insights into actionable patient engagement opportunities"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(
	["HAE", "Netherton Syndrome"]
)

for disease, tab in zip(
	["HAE", "Netherton Syndrome"],
	[tab1, tab2]
):

	with tab:

    	disease_df = df[
        	df["disease"] == disease
    	]

    	themes = (
        	disease_df[
            	~disease_df["theme"].isin(["Other"])
        	]["theme"]
        	.value_counts()
    	)

    	needs = (
        	disease_df[
            	~disease_df["unmet_need"].isin([
                	"Further Review Needed"
            	])
        	]["unmet_need"]
        	.value_counts()
    	)

    	if len(themes) == 0:
        	st.warning("No themes identified.")
        	continue

    	if len(needs) == 0:
        	st.warning("No unmet needs identified.")
        	continue

    	top_theme = themes.idxmax()
    	top_need = needs.idxmax()

    	opportunity = get_opportunity(
        	top_need
    	)

    	recommendations = get_recommendations(
        	top_need
    	)

    	top_need_count = needs.iloc[0]

    	priority = get_priority(
        	top_need_count
    	)

    	st.markdown(f"""
### **Top Theme**
**{top_theme}**

### **Top Unmet Need**
**{top_need}**

### **Priority**
**{priority}**

### **Patient Engagement Opportunity**
**{opportunity}**
""")

    	st.info(
        	f"""
The dominant conversation theme is **{top_theme}**, which maps to the unmet need **{top_need}**.

This suggests an opportunity in the area of **{opportunity}**.
"""
    	)

    	st.markdown("### **Recommended Actions**")

    	for item in recommendations:
        	st.write(f"• {item}")

    	# =====================================================
    	# PRIORITY RANKING
    	# =====================================================

    	st.markdown("---")

    	st.markdown("## 🚨 Theme Priority Ranking")

    	priority_rows = []

    	for theme_name, count in themes.items():

        	priority = get_priority(count)

        	if theme_name == "Access & Reimbursement":
            	need = "Access Barriers"

        	elif theme_name == "Diagnosis Journey":
            	need = "Healthcare System Friction"

        	elif theme_name == "Caregiver Burden":
            	need = "Emotional Burden"

        	elif theme_name == "Treatment Limitations":
            	need = "Treatment Limitations"

        	elif theme_name == "Treatment Experience":
            	need = "Treatment Limitations"

        	elif theme_name == "Disease Education":
            	need = "Healthcare System Friction"

        	else:
            	need = "Further Review Needed"

        	priority_rows.append({

            	"Theme": theme_name,

            	"Mentions": count,

            	"Priority": priority,

            	"Patient Engagement Opportunity":
                	get_opportunity(need)

        	})

    	priority_df = pd.DataFrame(priority_rows)

    	priority_df = priority_df.sort_values(
        	by="Mentions",
        	ascending=False
    	)

    	st.dataframe(
        	priority_df,
        	use_container_width=True,
        	hide_index=True
    	)
