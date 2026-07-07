# =====================================================
# THERAPEUTIC AREA TABS
# =====================================================

st.markdown("---")

tab1, tab2 = st.tabs([
    "HAE",
    "Netherton Syndrome"
])

# =====================================================
# HAE
# =====================================================

with tab1:

    st.header("HAE Platform Intelligence")

    hae_df = df[
        df["disease"] == "HAE"
    ]

    rows = []

    for platform in sorted(
        hae_df["platform"].unique()
    ):

        platform_df = hae_df[
            hae_df["platform"] == platform
        ]

        themes = (
            platform_df[
                ~platform_df["theme"].isin([
                    "Other"
                ])
            ]["theme"]
            .value_counts()
        )

        needs = (
            platform_df[
                ~platform_df["unmet_need"].isin([
                    "Further Review Needed"
                ])
            ]["unmet_need"]
            .value_counts()
        )

        top_theme = (
            themes.idxmax()
            if len(themes) > 0
            else "N/A"
        )

        top_need = (
            needs.idxmax()
            if len(needs) > 0
            else "N/A"
        )

        rows.append({

            "Platform": platform,

            "Posts": len(platform_df),

            "Top Theme": top_theme,

            "Top Unmet Need": top_need,

            "PE Opportunity":
                get_opportunity(top_need)

        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )

# =====================================================
# NETHERTON
# =====================================================

with tab2:

    st.header(
        "Netherton Syndrome Platform Intelligence"
    )

    ns_df = df[
        df["disease"] == "Netherton Syndrome"
    ]

    rows = []

    for platform in sorted(
        ns_df["platform"].unique()
    ):

        platform_df = ns_df[
            ns_df["platform"] == platform
        ]

        themes = (
            platform_df[
                ~platform_df["theme"].isin([
                    "Other"
                ])
            ]["theme"]
            .value_counts()
        )

        needs = (
            platform_df[
                ~platform_df["unmet_need"].isin([
                    "Further Review Needed"
                ])
            ]["unmet_need"]
            .value_counts()
        )

        top_theme = (
            themes.idxmax()
            if len(themes) > 0
            else "N/A"
        )

        top_need = (
            needs.idxmax()
            if len(needs) > 0
            else "N/A"
        )

        rows.append({

            "Platform": platform,

            "Posts": len(platform_df),

            "Top Theme": top_theme,

            "Top Unmet Need": top_need,

            "PE Opportunity":
                get_opportunity(top_need)

        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )
