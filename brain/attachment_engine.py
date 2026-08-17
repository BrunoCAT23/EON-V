class AttachmentEngine:
    def derive_attachment_style(self, relationship: dict) -> str:
        trust = relationship.get("trust", 0.1)
        familiarity = relationship.get("familiarity", 0.1)
        bond = relationship.get("bond_level", "new")

        if bond == "close" and trust >= 0.8:
            return "secure_close"

        if bond == "friend" and trust >= 0.5:
            return "warm_social"

        if familiarity >= 0.4:
            return "careful_opening"

        return "distant_polite"

    def build_attachment_summary(self, relationship: dict) -> str:
        style = self.derive_attachment_style(relationship)
        return f"attachment_style={style}"