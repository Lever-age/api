function CampaignInfo(attributes){
    this.campaign_id = attributes.campaign_id;
    this.election_year = attributes.election_year;
    this.candidate_id = attributes.candidate_id;
    this.candidate_position = attributes.candidate_position;
    this.candidate_party = attributes.candidate_party;
}

CampaignInfo.prototype.toJSON = function campaignInfoToJSON(){
    return {
        campaign_id: this.campaign_id,
        election_year: this.election_year,
        candidate_id: this.candidate_id,
        candidate_position: this.candidate_position,
        candidate_party: this.candidate_party
    };
}

module.exports = CampaignInfo;
