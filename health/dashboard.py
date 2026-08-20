from health.profile import get_profile
from health.checkins import get_recent_checkins


def generate_wellness_insights(checkins):
    """
    Generate simple wellness insights from recent check-ins.
    """

    if not checkins:
        return [
            {
                "type": "info",
                "icon": "🌱",
                "title": "Start Your Wellness Journey",
                "message": "Complete your first daily check-in to receive personalized wellness insights."
            }
        ]

    insights = []

    # ---------------- SLEEP ---------------- #

    sleep_values = []

    for checkin in checkins:
        try:
            sleep = float(checkin["sleep_hours"])

            if sleep >= 0:
                sleep_values.append(sleep)

        except (ValueError, TypeError, KeyError):
            pass

    if sleep_values:

        average_sleep = sum(sleep_values) / len(sleep_values)

        if average_sleep < 6:

            insights.append({
                "type": "warning",
                "icon": "😴",
                "title": "Sleep Needs Attention",
                "message": (
                    f"Your recent average sleep is {average_sleep:.1f} hours. "
                    "Consider maintaining a consistent sleep routine and getting adequate rest."
                )
            })

        elif average_sleep < 7:

            insights.append({
                "type": "info",
                "icon": "🌙",
                "title": "Improve Your Sleep",
                "message": (
                    f"Your recent average sleep is {average_sleep:.1f} hours. "
                    "A little more rest may help support your daily energy."
                )
            })

        else:

            insights.append({
                "type": "positive",
                "icon": "✨",
                "title": "Good Sleep Pattern",
                "message": (
                    f"Your recent average sleep is {average_sleep:.1f} hours. "
                    "Keep maintaining a consistent sleep routine."
                )
            })


    # ---------------- STRESS ---------------- #

    stress_values = []

    for checkin in checkins:

        try:
            stress = float(checkin["stress"])

            if 1 <= stress <= 5:
                stress_values.append(stress)

        except (ValueError, TypeError, KeyError):
            pass

    if stress_values:

        average_stress = sum(stress_values) / len(stress_values)

        if average_stress >= 4:

            insights.append({
                "type": "warning",
                "icon": "🧘",
                "title": "Stress Is Elevated",
                "message": (
                    "Your recent stress levels appear high. "
                    "Consider relaxation practices such as gentle breathing, meditation, "
                    "or taking short breaks during the day."
                )
            })

        elif average_stress >= 3:

            insights.append({
                "type": "info",
                "icon": "🌿",
                "title": "Manage Daily Stress",
                "message": (
                    "Your recent stress level is moderate. "
                    "Regular relaxation and mindful breathing may help."
                )
            })

        else:

            insights.append({
                "type": "positive",
                "icon": "😊",
                "title": "Stress Looks Balanced",
                "message": (
                    "Your recent stress levels appear relatively low. "
                    "Keep practicing habits that help you stay relaxed."
                )
            })


    # ---------------- ACTIVITY ---------------- #

    activity_values = []

    for checkin in checkins:

        try:
            activity = float(checkin["activity_minutes"])

            if activity >= 0:
                activity_values.append(activity)

        except (ValueError, TypeError, KeyError):
            pass

    if activity_values:

        average_activity = sum(activity_values) / len(activity_values)

        if average_activity < 20:

            insights.append({
                "type": "info",
                "icon": "🏃",
                "title": "Add More Movement",
                "message": (
                    f"Your recent average activity is {average_activity:.0f} minutes. "
                    "Consider adding gentle movement such as walking, stretching, or yoga."
                )
            })

        else:

            insights.append({
                "type": "positive",
                "icon": "🏃‍♀️",
                "title": "Good Activity",
                "message": (
                    f"Your recent average activity is {average_activity:.0f} minutes. "
                    "Keep staying active according to your comfort and ability."
                )
            })


    # ---------------- HYDRATION ---------------- #

    hydration_values = []

    hydration_score = {
        "Low": 1,
        "Moderate": 2,
        "Good": 3,
        "Excellent": 4
    }

    for checkin in checkins:

        hydration = checkin.get("hydration")

        if hydration in hydration_score:
            hydration_values.append(hydration_score[hydration])

    if hydration_values:

        average_hydration = (
            sum(hydration_values) / len(hydration_values)
        )

        if average_hydration < 2:

            insights.append({
                "type": "warning",
                "icon": "💧",
                "title": "Hydration Needs Attention",
                "message": (
                    "Your recent hydration ratings are low. "
                    "Remember to drink fluids regularly throughout the day."
                )
            })

        elif average_hydration >= 3:

            insights.append({
                "type": "positive",
                "icon": "💧",
                "title": "Good Hydration",
                "message": (
                    "Your recent hydration pattern looks good. "
                    "Keep maintaining regular hydration."
                )
            })


    # ---------------- DEFAULT ---------------- #

    if not insights:

        insights.append({
            "type": "info",
            "icon": "🌿",
            "title": "Keep Checking In",
            "message": (
                "Continue recording your wellness information so "
                "Dhanvantri can provide more personalized insights."
            )
        })


    return insights


def get_dashboard_data(user_id):
    """
    Collect all information needed by the wellness dashboard.
    """

    profile = get_profile(user_id)

    checkins = get_recent_checkins(user_id)

    insights = generate_wellness_insights(checkins)

    return {
        "profile": profile,
        "checkins": checkins,
        "insights": insights
    }