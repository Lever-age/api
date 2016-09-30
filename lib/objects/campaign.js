function Campaign(attributes){
    this.campaign_id = attributes.campaign_id;
    this.election_year = attributes.election_year;
    this.election_cycle = attributes.election_cycle;
    this.candidate_id = attributes.candidate_id;
    this.candidate_party = attributes.candidate_party;
    this.candidate_name = attributes.candidate_name;
    this.campaign_summary = attributes.campaign_summary;
}

Campaign.prototype.toJSON = function campaignToJSON(){
    return {
        campaign_id: this.campaign_id,
        election_year: this.election_year,
        election_cycle: this.election_cycle,
        candidate_id: this.candidate_id,
        candidate_party: this.candidate_party,
        candidate_name: this.candidate_name,
        campaign_summary: this.campaign_summary
    };
}

module.exports = Campaign;
