function CampaignSummary(attributes){
    this.campaign_id = attributes.campaign_id;
    this.summary_level = attributes.summary_level;
    this.summary_value = attributes.summary_value;
    this.summary_type = attributes.summary_type;
}

CampaignSummary.prototype.toJSON = function campaignSummaryToJSON(){
    return {
        campaign_id: this.campaign_id,
        summary_level: this.summary_level,
        summary_value: this.summary_value,
        summary_type: this.summary_type
    };
}

module.exports = CampaignSummary;
