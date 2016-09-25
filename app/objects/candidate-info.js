
function CandidateInfo(attrs){
  this.candidate_id   = attrs.candidate_id;
  this.candidate_name = attrs.candidate_name;
}

var CandidateInfo.prototype.toJSON = function(){
  return {
    candidate_id:   this.candidate_id,
    candidate_name: this.candidate_name
  }
};

module.exports = CandidateInfo;
