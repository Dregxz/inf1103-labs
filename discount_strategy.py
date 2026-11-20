from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class defining the discount strategy interface."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Returns the order total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Applies a percentage discount to the order total."""

    def __init__(self, percentage: float) -> None:
        pct = float(percentage)
        if pct < 0 or pct > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percentage: float = pct

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100.0)


class BulkDiscount(DiscountStrategy):
    """Subtracts a fixed amount when the order total meets or exceeds a threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        threshold_val = float(threshold)
        amount_val = float(amount)
        if threshold_val < 0 or amount_val < 0:
            raise ValueError("Bulk discount threshold and amount cannot be negative.")
        self.__threshold: float = threshold_val
        self.__amount: float = amount_val

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Applies a 5% student discount without modifying the Order class."""

    STUDENT_RATE: float = 5.0

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE / 100.0)
