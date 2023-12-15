#!/usr/local/bin/Rscript

total_score <- 0

f <- file("stdin")
open(f)
while (length(line <- readLines(f, n = 1)) > 0) {
  left <- gsub(".*: (.*) \\|.*", "\\1", line)
  right <- gsub(".*\\| (.*)", "\\1", line)

  left_values <- strsplit(left, split = " ") |> unlist()
  right_values <- strsplit(right, split = " ") |> unlist()

  winners <- intersect(left_values, right_values)

  # drop "" from winners, happens when there are two spaces
  # in a row, e.g., "58  5 54"
  winners <- winners[winners != ""]

  if (length(winners) > 0) {
    score <- 2^(length(winners) - 1)
    total_score <- total_score + score
  }
}

print(total_score)