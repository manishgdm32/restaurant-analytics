import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import src.analytics as analytics
from src.llm_utils import ask_ai

st.set_page_config(page_title="Lota Restaurant Analytics", layout="wide")

st.title("🍛 Lota Restaurant Analytics Dashboard")
st.markdown("**April 2026 Sales Data**")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "🍽️ Menu", "⏰ Timing", "🏷️ Discounts", "📦 Channels", "🤖 AI Chat"
])

with tab1:
    kpis = analytics.get_kpis()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
    col2.metric("Total Orders", kpis['total_orders'])
    col3.metric("Avg Order Value", f"${kpis['avg_order_value']:.2f}")
    col4.metric("Tips", f"${kpis['total_tips']:,.2f} ({kpis['tip_percentage']}%)")

    st.markdown("### Daily Revenue Trend")
    daily = analytics.get_daily_sales()
    fig = px.line(daily, x='Date', y='Amount', markers=True,
                  title="Daily Revenue", line_shape='spline')
    fig.update_layout(yaxis_title="Revenue ($)", xaxis_title="Date")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Sales by Day of Week")
    dow = analytics.get_daily_by_dayofweek()
    fig2 = px.bar(dow, x=dow.index, y=dow.values,
                  title="Revenue by Day of Week", color=dow.values,
                  color_continuous_scale='Viridis')
    fig2.update_layout(xaxis_title="Day", yaxis_title="Revenue ($)")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown("### Top Selling Items")
    top_items = analytics.get_top_items(15)
    fig = px.bar(top_items, x=top_items.values, y=top_items.index, orientation='h',
                 title="Top 15 Items by Revenue", color=top_items.values,
                 color_continuous_scale='Plasma')
    fig.update_layout(yaxis_title="Item", xaxis_title="Revenue ($)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Category Breakdown")
    cat = analytics.get_category_sales()
    fig2 = px.pie(values=cat.values, names=cat.index,
                  title="Sales by Category", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Menu Group Performance")
    group = analytics.get_menu_group_performance()
    st.dataframe(group, use_container_width=True)

with tab3:
    st.markdown("### Hourly Sales Distribution")
    hourly = analytics.get_hourly_sales()
    fig = px.bar(hourly, x='Hour', y='Amount',
                 title="Revenue by Hour of Day",
                 color='Amount', color_continuous_scale='RdYlGn')
    fig.update_layout(xaxis_title="Hour (0-23)", yaxis_title="Revenue ($)")
    fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Peak Hours Heatmap")
    data = analytics.get_data()
    orders = data['valid_orders']
    pivot = orders.pivot_table(index='Hour', columns='DayOfWeek',
                               values='Amount', aggfunc='sum', fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(columns=day_order)

    fig2 = px.imshow(pivot, labels=dict(x="Day of Week", y="Hour", color="Revenue"),
                     color_continuous_scale='YlOrRd', aspect='auto')
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.markdown("### Discount Impact by Channel")
    disc = analytics.get_discount_impact()
    st.dataframe(disc, use_container_width=True)

    fig = px.bar(disc, x='Dining Option', y='Net Sales',
                 title="Net Sales by Channel",
                 color='Discount %', color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Discount Effectiveness")
    for idx, row in disc.iterrows():
        st.write(f"**{row['Dining Option']}**: ${row['Net Sales']:.2f} revenue, "
                 f"${row['Discount Amount']:.2f} discounts ({row['Discount %']}%)")

with tab5:
    st.markdown("### Channel Performance")
    channel = analytics.get_channel_performance()
    st.dataframe(channel, use_container_width=True)

    fig = px.pie(channel, values='Net Sales', names='Dining Option',
                 title="Revenue by Channel", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Server Performance")
    server = analytics.get_server_performance()
    st.dataframe(server, use_container_width=True)

    payout = analytics.get_payout_summary()
    st.markdown(f"**Total Payouts**: ${payout['total_payouts']:,.2f} | "
                f"**Total Fees**: ${payout['total_fees']:,.2f}")

with tab6:
    st.markdown("### 🤖 Ask AI for Business Insights")
    st.write("Ask questions like:")
    st.info("• Which dishes should I promote?")
    st.info("• When should I add more staff?")
    st.info("• Are my discounts effective?")
    st.info("• What's my best performing category?")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    question = st.text_input("Ask a question:", placeholder="e.g., What should I do to increase profit?")

    if question:
        with st.spinner("Analyzing..."):
            try:
                response = ask_ai(question)
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": response
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("### Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**You**: {chat['question']}")
        st.markdown(f"**AI**: {chat['answer']}")
        st.divider()