//
//  SignaDesign.swift
//  Signa
//
//  Visual system for Signa. Feather remains the underlying signing engine.
//

import SwiftUI

enum SignaTheme {
	static let accent = Color(.sRGB, red: 1.0, green: 0.435, blue: 0.102, opacity: 1.0)
	static let accentSoft = Color(.sRGB, red: 1.0, green: 0.62, blue: 0.30, opacity: 1.0)
	static let cornerRadius: CGFloat = 24

	static var ambientGradient: LinearGradient {
		LinearGradient(
			colors: [accentSoft.opacity(0.20), accent.opacity(0.055), .clear],
			startPoint: .topLeading,
			endPoint: .bottomTrailing
		)
	}
}

private struct SignaGlassCard: ViewModifier {
	var cornerRadius: CGFloat = SignaTheme.cornerRadius
	var selected = false

	func body(content: Content) -> some View {
		if #available(iOS 26.0, *) {
			content
				.glassEffect(
					.regular.tint(SignaTheme.accent.opacity(selected ? 0.16 : 0.055)),
					in: .rect(cornerRadius: cornerRadius)
				)
				.overlay {
					RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
						.strokeBorder(
							selected ? SignaTheme.accent.opacity(0.8) : Color.white.opacity(0.18),
							lineWidth: selected ? 1.5 : 0.5
						)
				}
		} else {
			content
				.background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
				.overlay {
					RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
						.strokeBorder(
							selected ? SignaTheme.accent : Color.primary.opacity(0.08),
							lineWidth: selected ? 2 : 0.5
						)
				}
		}
	}
}

private struct SignaProminentButton: ViewModifier {
	func body(content: Content) -> some View {
		if #available(iOS 26.0, *) {
			content.buttonStyle(.glassProminent)
		} else {
			content.buttonStyle(.borderedProminent)
		}
	}
}

private struct SignaStandardButton: ViewModifier {
	func body(content: Content) -> some View {
		if #available(iOS 26.0, *) {
			content.buttonStyle(.glass)
		} else {
			content.buttonStyle(.bordered)
		}
	}
}

struct SignaTabBarBehavior: ViewModifier {
	func body(content: Content) -> some View {
		if #available(iOS 26.0, *) {
			content.tabBarMinimizeBehavior(.onScrollDown)
		} else {
			content
		}
	}
}

extension View {
	func signaGlassCard(cornerRadius: CGFloat = SignaTheme.cornerRadius, selected: Bool = false) -> some View {
		modifier(SignaGlassCard(cornerRadius: cornerRadius, selected: selected))
	}

	func signaProminentButton() -> some View {
		modifier(SignaProminentButton())
	}

	func signaStandardButton() -> some View {
		modifier(SignaStandardButton())
	}
}
