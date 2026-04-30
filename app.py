# =========================
# 🔥 INSIGHTS DISPLAY (UPGRADED)
# =========================
if "insights" in data:
    insights = data["insights"]

    st.subheader("⚡ AI Energy Intelligence")

    # 🎯 TOP METRICS (CLEAN UI)
    col1, col2, col3 = st.columns(3)

    col1.metric("Peak Risk", insights.get("peak_risk", "N/A"))
    col2.metric("Alert Status", insights.get("alert", "N/A"))
    col3.metric("Cost Impact", insights.get("cost_impact", "N/A"))

    # 💰 COST SECTION
    st.markdown("### 💰 Estimated Cost Impact")
    st.success(f"${insights.get('estimated_cost', 0):.2f}")

    # 🚨 ALERT COLOR LOGIC (IMPORTANT UX)
    alert = insights.get("alert", "NORMAL")

    if alert == "HIGH":
        st.error(f"🚨 ALERT: {alert}")
    elif alert == "MEDIUM":
        st.warning(f"⚠️ ALERT: {alert}")
    else:
        st.success(f"✅ ALERT: {alert}")

    # 🧠 RECOMMENDATION
    st.markdown("### 🧠 Recommended Action")
    st.info(insights.get("recommendation", "No recommendation"))

    # 💡 SAVINGS TIP
    st.markdown("### 💡 Optimization Tip")
    st.warning(insights.get("savings_tip", "No tip available"))
