from typing import List, Tuple, Optional
from django.db import models
from company.models import CurrentOpening
from user.models import Student
from django.core.exceptions import ValidationError

# Create your models her


class PlacedDetails(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ctc_lpa = models.FloatField()
    offer_letter = models.FileField(upload_to="offerletters")

    def save(self) -> None:
        return super().save()

    class Meta:
        abstract = True


class OnCampusPlacedDetail(PlacedDetails):
    # DO NOT manage automatically based on other details
    offer = models.ForeignKey(CurrentOpening, on_delete=models.CASCADE)


class OffCampusPlacedDetail(PlacedDetails):
    company = models.CharField(max_length=256)


class StudentOpening(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    opening = models.ForeignKey(CurrentOpening, on_delete=models.CASCADE)
    # ADD entry only if the student applied in the opening, this makes the `applied` boolean redundant
    applied = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    first_round = models.BooleanField(default=False)
    second_round = models.BooleanField(default=False)
    third_round = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def sequential_validation(self, arr: List[Tuple[str, bool]]) -> Optional[int]:
        false_occured = False
        for idx, (_, current) in enumerate(arr):
            if not false_occured and not current:
                false_occured = True
            if current and false_occured:
                return idx

        return None

    def clean(self):
        # TODO : some companies only have 1 round, student might directly be selected, hence round2 and 3 are false/null
        # this wont be saved in db, either normalise the db to accomodate arbitrary number of rounds
        # or make a better check
        sequence = [
            ("applied", self.applied),
            ("present", self.present),
            ("first_round", self.first_round),
            ("second_round", self.second_round),
            ("third_round", self.third_round),
            ("selected", self.selected),
            ("accepted", self.accepted),
        ]
        key = self.sequential_validation(sequence)
        if key is not None:
            raise ValidationError(
                {
                    sequence[key][
                        0
                    ]: f"{sequence[key][0]} cannot be true since {sequence[key-1][0]} is false"
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.student.is_selected = bool(StudentOpening.objects.filter(selected=True))
        self.student.save()

    class Meta:
        verbose_name = "Student Opening"
        verbose_name_plural = "Student Openings"

    def __str__(self) -> str:
        return f"{self.student} {self.opening}"
