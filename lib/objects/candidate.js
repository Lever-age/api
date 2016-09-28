function Candidate(attributes){
    this.candidate_id = attributes.candidate_id;
    this.candidate_name = attributes.candidate_name;
    this.campaigns = attributes.campaigns;
}

Candidate.prototype.toJSON = function candidateToJSON(){
    return {
        candidate_id: this.candidate_id,
        candidate_name: this.candidate_name,
        campaigns: this.campaigns
    };
}

module.exports = Candidate;
