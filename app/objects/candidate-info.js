function CandidateInfo(attributes){
    this.candidate_id = attributes.candidate_id;
    this.candidate_name = attributes.candidate_name;
}

CandidateInfo.prototype.toJSON = function candidateInfotoJSON(){
    return {
        candidate_id: this.candidate_id,
        candidate_name: this.candidate_name
    };
}

module.exports = CandidateInfo;