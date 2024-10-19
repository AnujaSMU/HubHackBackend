from pydantic import BaseModel, Field
from typing import List, Union
from datetime import date

class ChangesModel(BaseModel):
    id : str = Field(None, title="Program ID", description="Unique Identifier")
    program_name: str = Field(..., title="Program Name", description="Single-Line Text Field")
    description: str = Field(None, title="Description", description="Multi-Line Text Field")
    delivery_method: str = Field("In-person", title="Delivery Method", description="Single-Line Text Field")
    status: str = Field("Active", title="Status", description="Drop-down")
    funders: List[str] = Field(["Health Department", "Local NGOs"], title="Funders", description="Multi-choice selection")
    end_date: date = Field("2024-12-31", title="End Date", description="DatePicker")
    team: str = Field("Health Outreach", title="Team", description="Drop-down list")
    other_eligibility_criteria: str = Field(None, title="Other Eligibility Criteria", description="Multi-line TextBox")
    geographic_availability: str = Field("Citywide", title="Geographic Availability", description="Single-Line Text Box")
    literacy_requirement: str = Field(None, title="Literacy Requirement", description="Single-Line Text Box")
    age_targeting: str = Field(None, title="Age Targeting", description="Single Line Text Field (single age or range)")
    gender_targeting: str = Field(None, title="Gender Targeting", description="Single Line Text Field")
    staff_member_names: List[str] = Field(None, title="Staff Member Names", description="Names of People (from Active Directory)")
    eligibility: Union[List[str], str] = Field(..., title="Eligibility", description="Eligibility criteria with option for new criteria")
    change_status: str = Field("Pending", title="Change Status", description="Drop-down")