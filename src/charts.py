import plotly.express as px


def skills_pie_chart(found, missing):

    labels = ["Matched Skills", "Missing Skills"]

    values = [len(found), len(missing)]

    fig = px.pie(
        names=labels,
        values=values,
        title="Skills Analysis"
    )

    return fig


def score_bar_chart(ats_score, jd_score):

    fig = px.bar(
        x=["ATS Score", "JD Match"],
        y=[ats_score, jd_score],
        title="Resume Performance"
    )

    return fig