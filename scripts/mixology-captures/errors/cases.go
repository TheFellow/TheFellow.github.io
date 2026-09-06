// Package deckcapture supplies failures for the deck's presentation examples.
package deckcapture

import (
	"context"

	"github.com/TheFellow/go-modular-monolith/app"
	models "github.com/TheFellow/go-modular-monolith/app/domains/ingredients/models"
	"github.com/TheFellow/go-modular-monolith/app/kernel/measurement"
	"github.com/TheFellow/go-modular-monolith/pkg/errors"
	"github.com/TheFellow/go-modular-monolith/pkg/presentation/actions"
)

func MissingNameIngredient() *models.Ingredient {
	ingredient := DuplicateIngredient()
	ingredient.Name = ""
	return ingredient
}

func DuplicateIngredient() *models.Ingredient {
	return &models.Ingredient{Name: "London Dry Gin", Category: models.CategorySpirit, Unit: measurement.UnitOz}
}

// InternalFailure reproduces the explicitly injected example in chapter 1.3.
// The failure is injected; action evaluation and wrapping are real.
func InternalFailure() error {
	failure := errors.Internalf("load readiness: %w", errors.New("database is locked")).
		WithUserMessage("Readiness is temporarily unavailable")
	_, err := actions.Evaluate(context.Background(), actions.Group{
		Permission: actions.Public(),
		Controls: []actions.Control{{ID: "publish", Conditions: []actions.Condition{
			func(context.Context) (bool, string, error) { return false, "", failure },
		}}},
	})
	return err
}

type Case struct {
	Name  string
	Err   error
	Kind  errors.Kind
	Exit  int
	Style errors.TUIStyle
}

func Cases(session *app.Session) []Case {
	_, invalid := session.Ingredients.Create(session.Context(), MissingNameIngredient())
	_, conflict := session.Ingredients.Create(session.Context(), DuplicateIngredient())
	return []Case{
		{"invalid", invalid, errors.KindInvalid, 10, errors.TUIStyleError},
		{"conflict", conflict, errors.KindConflict, 40, errors.TUIStyleWarning},
		{"internal", InternalFailure(), errors.KindInternal, 50, errors.TUIStyleError},
	}
}
