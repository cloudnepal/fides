from datetime import datetime, timezone

from fides.api.models.privacy_notice import UserConsentPreference
from fides.api.models.privacy_preference import (
    ConsentIdentitiesMixin,
    LastServedNotice,
    PrivacyPreferenceHistory,
    ServedNoticeHistory,
    ServingComponent,
)


class TestPrivacyPreference:

    def test_privacy_notice_preference(
        self,
        db,
        privacy_experience_privacy_center,
        privacy_notice_us_ca_provide,
        served_notice_history,
        property_a,
    ):
        received = datetime.utcnow()
        preference_history_record = PrivacyPreferenceHistory.create(
            db=db,
            data={
                "anonymized_ip_address": "92.158.1.0",
                "email": "test@email.com",
                "method": "button",
                "privacy_experience_config_history_id": privacy_experience_privacy_center.experience_config.translations[
                    0
                ].privacy_experience_config_history_id,
                "preference": "opt_in",
                "privacy_notice_history_id": privacy_notice_us_ca_provide.translations[
                    0
                ].privacy_notice_history_id,
                "received_at": received,
                "request_origin": "privacy_center",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/324.42 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/425.24",
                "user_geography": "us_ca",
                "url_recorded": "https://example.com/privacy_center",
                "served_notice_history_id": served_notice_history.served_notice_history_id,
                "property_id": property_a.id,
            },
            check_name=False,
        )

        assert preference_history_record.preference == UserConsentPreference.opt_in
        assert (
            preference_history_record.privacy_notice_history_id
            == privacy_notice_us_ca_provide.translations[0].histories[0].id
        )
        assert (
            preference_history_record.privacy_notice_history
            == privacy_notice_us_ca_provide.translations[0].histories[0]
        )
        assert preference_history_record.property_id == property_a.id
        assert preference_history_record.received_at is not None
        assert (
            preference_history_record.received_at.tzinfo
            == preference_history_record.created_at.tzinfo
            == timezone.utc
        )

        preference_history_record.delete(db)

    def test_tcf_preference(self, db, privacy_experience_france_overlay, property_a):
        preference_history_record = PrivacyPreferenceHistory.create(
            db=db,
            data={
                "anonymized_ip_address": "92.158.1.0",
                "email": "test@email.com",
                "fides_user_device": "051b219f-20e4-45df-82f7-5eb68a00889f",
                "method": "accept",
                "privacy_experience_config_history_id": None,
                "preference": "tcf",
                "request_origin": "tcf_overlay",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/324.42 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/425.24",
                "user_geography": "fr_idg",
                "url_recorded": "example.com/",
                "served_notice_history_id": "served_notice_history_test_id",
                "tcf_preferences": {
                    "purpose_consent_preferences": [{"id": 1, "preference": "opt_out"}],
                    "purpose_legitimate_interests_preferences": [
                        {"id": 1, "preference": "opt_in"},
                        {"id": 2, "preference": "opt_in"},
                    ],
                    "vendor_consent_preferences": [
                        {"id": "gvl.8", "preference": "opt_out"}
                    ],
                    "vendor_legitimate_interests_preferences": [],
                    "special_feature_preferences": [],
                    "special_purpose_preferences": [],
                    "feature_preferences": [],
                    "system_legitimate_interests_preferences": [],
                },
                "property_id": property_a.id,
            },
        )
        assert preference_history_record.preference == UserConsentPreference.tcf
        assert preference_history_record.privacy_notice_history_id is None
        assert preference_history_record.tcf_preferences == {
            "purpose_consent_preferences": [{"id": 1, "preference": "opt_out"}],
            "purpose_legitimate_interests_preferences": [
                {"id": 1, "preference": "opt_in"},
                {"id": 2, "preference": "opt_in"},
            ],
            "vendor_consent_preferences": [{"id": "gvl.8", "preference": "opt_out"}],
            "vendor_legitimate_interests_preferences": [],
            "special_feature_preferences": [],
            "special_purpose_preferences": [],
            "feature_preferences": [],
            "system_legitimate_interests_preferences": [],
        }
        assert preference_history_record.property_id == property_a.id

        preference_history_record.delete(db)


class TestConsentIdentitiesHashMixin:
    def test_hash_value_null(self):
        assert ConsentIdentitiesMixin.hash_value("") is None

    def test_hash_value_not_null(self):
        assert ConsentIdentitiesMixin.hash_value("customer_one@example.com") is not None


class TestServedNoticeHistory:
    def test_get_by_served_id(self, served_notice_history, db):
        """Assert looked up by served id field, not id"""
        assert ServedNoticeHistory.get_by_served_id(db, "ser_12345").all() == [
            served_notice_history
        ]

        assert (
            ServedNoticeHistory.get_by_served_id(db, served_notice_history.id).all()
            == []
        )

    def test_create(self, db, privacy_notice):
        served = ServedNoticeHistory.create(
            db=db,
            data={
                "acknowledge_mode": False,
                "serving_component": ServingComponent.overlay,
                "privacy_notice_history_id": privacy_notice.translations[
                    0
                ].privacy_notice_history_id,
                "email": "test@example.com",
                "received_at": datetime.utcnow(),
                "hashed_email": ConsentIdentitiesMixin.hash_value("test@example.com"),
                "served_notice_history_id": "ser_12345",
            },
            check_name=False,
        )
        assert served.received_at is not None
        assert served.received_at.tzinfo == served.created_at.tzinfo == timezone.utc

        served.delete(db)


class TestServedNoticeHistoryId:
    def test_generate_served_notice_history_id(self):
        assert LastServedNotice.generate_served_notice_history_id().startswith("ser_")
